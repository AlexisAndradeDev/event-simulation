from collections import defaultdict

class SimulationState:
    """
    Represents the state of the simulation.

    Attributes:
        future_events (list): The list of future events (pending processing)
            sorted by their scheduled time.
        current_time (float): The current simulation time, same unit of
            time as T passed to `simulate_case`.
        client_id (int): The ID for the current client being processed.
        waits (defaultdict(list)): A dictionary mapping node names to lists
            of wait times in queue experienced by clients at those nodes.
    """
    def __init__(self):
        self.future_events = []
        self.current_time = 0.0
        self.client_id = 0
        self.waits = defaultdict(list)
