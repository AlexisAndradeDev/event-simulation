from collections import deque

class Node:
    def __init__(self, name: str, mu: float, servers: int, external_lambda=0):
        """
        Initialize a Node representing a service station in a queueing system.

        Args:
            name (str): The identifier or name of the node.
            mu (float): Service rate of each individual server in this node.
            servers (int): Number of parallel servers at the node.
            external_lambda (float, optional): Arrival rate of external
                customers to the node. Defaults to 0 (no external arrivals).
        """
        self.name = name
        self.mu = mu # service rate of each server
        self.servers = servers # number of servers
        self.external_lambda = external_lambda
        self.busy = 0 # current number of busy servers
        # Queue of clients waiting for service, elements are a tuple
        # (client_id, arrival_time_to_queue).
        self.queue = deque()

        # statistics
        self.area_q = 0.0 # integral of queue length over time
        self.area_busy = 0.0 # integral of busy servers over time
        self.num_served = 0 # total number of clients served by the node
