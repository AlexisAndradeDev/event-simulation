class Event:
    def __init__(self, time, kind, node_name, client_id, external=False):
        self.time = time # time of the event
        self.kind = kind # 'arrival' or 'departure'
        self.node_name = node_name # node where the event occurs
        self.client_id = client_id # client identifier
        self.external = external # whether it's an external arrival

    def __lt__(self, other):
        """
        This method is used to perform 'less than' comparisons between Event objects.

        heapq.heappush() and heapq.heappop() use the __lt__ method of the contained
        objects to maintain their elements in ascending order. In our case, we want the
        future events list sorted by event time from smallest to largest.

        >>> event1 = Event(1, 'arrival', 'node1', 1)
        >>> event2 = Event(2, 'arrival', 'node1', 2)
        >>> event1 < event2
        True
        """
        return self.time < other.time