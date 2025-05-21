from collections import deque

class Node:
    def __init__(self, name, mu, servers):
        self.name = name
        self.mu = mu # service rate of each server
        self.servers = servers # number of servers
        self.busy = 0 # busy servers
        self.queue = deque() # queue of clients (client_id, arrival_time_to_queue)

        # statistics
        self.area_q = 0.0 # integral of queue length over time
        self.area_busy = 0.0 # integral of busy servers over time
        self.num_served = 0 # total number of served clients
