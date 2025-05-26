from collections import deque

class Node:
    def __init__(self, name: str, mu: float, servers: int,
            routing_probabilities: dict[str, float],
            external_lambda: float = 0):
        """
        Initialize a Node representing a service station in a queueing system.

        Args:
            name (str): The identifier or name of the node.
            mu (float): Service rate of each individual server in this node.
            servers (int): Number of parallel servers at the node.
            external_lambda (float, optional): Arrival rate of external
                customers to the node. Defaults to 0 (no external arrivals).
            routing_probabilities (dict[str, float]): A dictionary mapping the
                names of other nodes to the probability of routing a customer
                to that node after service completion. The probabilities should
                sum to 1 or less, where the remaining probability (if any)
                represents customers leaving the system after service.
                
                For example, if you have 5 nodes, and Node1 routes to
                Node2 or Node3, routing_probabilities will be
                {'Node2': prob1, 'Node3': prob2}.
                
                If it's an empty dict, the clients always leave the system
                after this node.
        """
        self.name = name
        self.mu = mu
        self.servers = servers
        self.routing_probabilities = routing_probabilities
        self.external_lambda = external_lambda
        self.busy = 0 # current number of busy servers
        # Queue of clients waiting for service, elements are a tuple
        # (client_id, arrival_time_to_queue).
        self.queue = deque()

        # statistics
        self.area_q = 0.0 # integral of queue length over time
        self.area_busy = 0.0 # integral of busy servers over time
        self.num_served = 0 # total number of clients served by the node
