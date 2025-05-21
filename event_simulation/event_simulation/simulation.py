import random
import json
import heapq
import pandas as pd
from tabulate import tabulate
from pathlib import Path
from collections import defaultdict
from event_simulation.node import Node
from event_simulation.event import Event

def save_simulation(simulation_name: str, run_dir: Path,
        metrics: dict[str, dict[str, float]], nodes: dict[str, Node],
        lambda1: float, lambda2: float, T: float, seed: int) -> None:
    simulation_dir = run_dir / simulation_name
    simulation_dir.mkdir(parents=True, exist_ok=True)

    metrics_df = pd.DataFrame(metrics).T.round(4)
    metrics_df = metrics_df[['Wq', 'W', 'Lq', 'L', 'rho']]
    results_path = simulation_dir / 'simulation_results.csv'
    metrics_df.to_csv(results_path)
    print(f"Results of the simulation {simulation_name} saved in '{results_path}'.")

    params = {
        'seed': seed,
        'nodes': {name: {'mu': node.mu, 'servers': node.servers} for name, node in nodes.items()},
        'lambda1': lambda1,
        'lambda2': lambda2,
        'T': T,
    }
    params_path = simulation_dir / 'simulation_params.json'
    with params_path.open('w') as f:
        json.dump(params, f, indent=4)
    print(f"Simulation parameters for {simulation_name} saved in '{params_path}'.")

def display_simulation_metrics(simulation_name: str, metrics: dict[str, dict[str, float]]):
    # Convert simulation results to a DataFrame and display it as a table
    df = pd.DataFrame(metrics).T
    # Format all floats to 4 decimal places as strings for display
    formatted_df = df.applymap(lambda x: f"{x:.4f}")
    print(f"Simulation results: {simulation_name}")
    print(tabulate(formatted_df, headers='keys', tablefmt='grid', showindex=True))

def simulate_case(case_name: str, T: float, lambda1: float, lambda2: float,
        nodes: dict[str, Node], p_to_consult1: float = None,
        show_simulation_metrics: bool = True,
        save_results: bool = False, run_dir: Path = None, seed: int = None,
        ) -> dict[str, dict[str, float]]:
    """
    Queueing system simulation.
    
    Args:
        case_name: Name of the simulation case.
        T: Simulation time (hours).
        lambda1: External arrival rate to 'reg1' (patients/hour).
        lambda2: External arrival rate to 'reg2' (patients/hour).
        nodes: Dictionary <name, Node>
        p_to_consult1: Probability that a patient goes to 'consult1'
            from an examination room. Only if case_name is 'solution3',
            'solution4', or 'solution5', otherwise None.
        show_simulation_metrics: If True, simulation metrics are shown
            at the end. Default is True.
        save_results: If True, simulation results are saved in a CSV file
            and simulation parameters in a JSON file. Default is False.
        run_dir: Path to the directory where simulation results will be saved.
            Must exist. Default is None.
        seed: Seed for random number generation.
    
    Returns:
        metrics: Dictionary <node_name, dict<metric_name, float>>
            Explanation of the metrics:
            - Wq: Average client in queue time (hours).
            - W: Average client in system time (hours).
            - Lq: Average queue length (number of customers in queue).
            - L: Average system length (number of customers in system).
            - rho: Proportion of time servers are busy.
            - throughput: Throughput (number of customers served per hour).
    """
    print(f"------ Simulación '{case_name}' ------")

    if save_results:
        assert run_dir is not None, "run_dir cannot be None if save_results is True."
        assert seed is not None, "seed cannot be None if save_results is True."
        assert run_dir.exists(), f"run_dir '{run_dir}' does not exist."

    # future_events is the list of future events (pending processing)
    # sorted by time
    future_events = []
    # Current simulation time (goes from 0 to T, in hours)
    current_time = 0.0
    # Client ID for the current event
    client_id = 0
    # Dictionary whose keys are node names
    # The value for each key is the list of times each client waited in
    # queue at that node
    waits = defaultdict(list)

    # A heap is used to handle the future events list.
    # This way, events are ordered from smallest to largest time
    # (instant when they occur, stored in event.time).
    # The event with the smallest time is the first to be popped using
    # heappop (which removes and returns the first element of the list).

    # First external arrivals to reg1 and reg2
    heapq.heappush(
        future_events, 
        Event(current_time+random.expovariate(lambda1), 'arrival', 'reg1', client_id, True),
    )
    client_id += 1

    heapq.heappush(
        future_events,
        Event(current_time+random.expovariate(lambda2), 'arrival', 'reg2', client_id, True),
    )
    client_id += 1

    # Process future events until no more events exist
    # or until the event time is greater than the maximum simulation time (T)
    while future_events:
        event: Event = heapq.heappop(future_events)

        if event.time > T:
            break

        # Advance simulation clock
        time_passed_since_last_event = event.time - current_time
        current_time = event.time

        # Update areas (integrals)
        # (Used to calculate performance metrics exactly for the simulation)
        for nd in nodes.values():
            nd.area_q += len(nd.queue) * time_passed_since_last_event
            nd.area_busy += nd.busy * time_passed_since_last_event

        node = nodes[event.node_name]

        # If the event is an arrival, attend to the client
        if event.kind == 'arrival':
            # If it is an external arrival, generate a new arrival event
            # to generate a new external client.
            # Between each external client, wait a random time
            # following an exponential distribution with rate lambda.
            # Each external arrival event passes through this code section
            # only once, when it first arrives to the system.
            if event.external:
                lam = lambda1 if event.node_name == 'reg1' else lambda2
                # Create new external arrival event (new client)
                heapq.heappush(
                    future_events,
                    Event(
                        current_time+random.expovariate(lam), 'arrival',
                        event.node_name, client_id, True,
                    ),
                )
                client_id += 1

            # If the node has available servers, attend the client
            # and generate a departure event for them
            if node.busy < node.servers:
                node.busy += 1
                waits[node.name].append(0.0) # no queue wait
                # service time until the client departs
                service_time = random.expovariate(node.mu)
                heapq.heappush(
                    future_events,
                    Event(
                        current_time+service_time, 'departure', node.name,
                        event.client_id,
                    )
                )
            # If the node has all servers busy, add to the queue
            # and wait for a server to become free
            else:
                node.queue.append((event.client_id, current_time))

        # If the event is a departure
        else:
            # The client being served in this node finishes now

            node.num_served += 1
            node.busy -= 1

            # If there are clients in the node's queue
            if node.queue:
                # Attend the next client in the queue
                next_client_in_queue_id, time_the_next_client_in_queue_arrived = \
                    node.queue.popleft()

                # Add the time this next client waited in queue
                # to the wait times list
                waits[node.name].append(current_time - time_the_next_client_in_queue_arrived)

                node.busy += 1
                # service time until this next client departs
                service_time = random.expovariate(node.mu)
                heapq.heappush(
                    future_events,
                   Event(
                        current_time+service_time, 'departure', node.name,
                        next_client_in_queue_id,
                    )
                )

            # Route to the next node
            if event.node_name.startswith('reg'):
                if case_name in ['base', 'solution3', 'solution4']:
                    # Will go to the examination room corresponding
                    # to the registration room number
                    # reg2 -> exam2
                    next_node_name = event.node_name.replace('reg', 'exam')
                elif case_name in ['solution5']:
                    # All registration rooms go to the same
                    # single examination room
                    next_node_name = 'exam'
            elif event.node_name.startswith('exam'):
                if case_name in ['base']:
                    # Will go to the consultation room corresponding
                    # to the examination room number
                    # consult2 -> exam2
                    next_node_name = event.node_name.replace('exam', 'consult')
                elif case_name in ['solution3', 'solution4', 'solution5']:
                    # Routing with probability
                    # There is a probability p_to_consult1 that the patient
                    # goes to consult1 and 1 - p_to_consult1 that they
                    # go to consult2
                    next_node_name = (
                        'consult1' if random.random() < p_to_consult1
                        else 'consult2'
                    )
            elif event.node_name.startswith('consult'):
                # After consultation, leaves the system
                # Skip to the next iteration of future_events
                # without generating an arrival event to the next node for
                # this client
                continue
            else:
                raise ValueError(f"Nombre de nodo {event.node_name} en evento de salida {event.client_id} inesperado.")

            # Generate an arrival event at the next node for the current
            # client (client leaves current node and arrives at the next)
            heapq.heappush(
                future_events,
                Event(
                    current_time, 'arrival', next_node_name, event.client_id, False
                )
            )

    # Calculate metrics for each node
    metrics = {}
    for name, nd in nodes.items():
        Lq = nd.area_q / T
        L = nd.area_q / T + nd.area_busy / T
        rho = nd.area_busy / T / nd.servers
        Wq = sum(waits[name]) / len(waits[name]) if waits[name] else 0.0
        W = L / (nd.num_served / T) if nd.num_served > 0 else 0.0
        # throughput is the number of customers served per hour at the node
        # (number of customers served by the node / simulation time in hours)
        X = nd.num_served / T

        metrics[name] = {
            'Wq': Wq,
            'W': W,
            'Lq': Lq,
            'L': L,
            'rho': rho,
            'throughput': X
        }
    
    if show_simulation_metrics:
        display_simulation_metrics(case_name, metrics)
    if save_results:
        save_simulation(case_name, run_dir, metrics, nodes, lambda1, lambda2, T, seed)

    return metrics
