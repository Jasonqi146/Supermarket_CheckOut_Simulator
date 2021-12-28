import numpy as np
from queue import PriorityQueue
from .grocery_store import GroceryStore
from .event import *

class Simulator:
    """A grocery store Simulator.

    The Simulator sets up and runs a simulation to obtain several metrics.
    
    === Attributes ===
    @type events: PriorityQueue[Event]
        A sequence of events arranged in priority determined by the event
        sorting order.
    @type store: GroceryStore
        The grocery store associated with the simulator.
    @type random_state: int
        A random state seed to run simulation for generaing fixed outputs;
        nullable.
    @type _finished: bool
        If the simulator has finished processing events.
    """
    
    def __init__(self, store_config, random_state=None):
        """Initialize a GroceryStoreSimulation from store_config dict.

        @type store_config: dict[str, int]
            A mapping from each checkout line type to how many there are.
        @rtype: None
        """
        self.events = PriorityQueue()
        self.store = GroceryStore(store_config)
        self.random_state = random_state
        self._finished = False
        
    def run(self, initial_events_str):
        """Run the simulation on the events defined by initial_events_str.

        Return a dictionary containing statistics of the simulation.

        @type self: GroceryStoreSimulation
        @type initial_events_str: str
            A line-separated string to represent a list of initial events.
        @rtype: None
        """
        
        assert not self._finished, "Error: the simulator has finished running;" \
        + " please initialize a new Simulator object."
        
        if self.random_state is not None:
            np.random.seed(self.random_state)

        initial_events = create_event_list(initial_events_str, self.store)
        for event in initial_events:
            self.events.put(event)

        while not self.events.empty():
            future_events = self.events.get().do(self.store)
            for future_event in future_events:
                self.events.put(future_event)
        
        self._finished = True
    
    def query_statistics(self, criterion="wait", start_time=None, end_time=None,
                         line_ids=None, filter_by="join"):
        """Query a specific type of statistics during the simulation, within an
        optional interval and/or given an optional list of checkout lines.
        
        If start_time or end_time is not given, assume full duration.
        Time bounds are based on customers' **join time** by default.
        
        @type self: GroceryStoreSimulation
        @type criterion:
            Can be one of the following:
                "wait": wait time before checkout
                "checkout": checkout duration time
                "total": wait + checkout
        @type start_time: int
            Left bound (inclusive) to calculate statistics.
        @type end_time: int
            Right bound (exclusive) to calculate statistics.
        @type filter_by: str
            Specifies which timestamp to use for filtering
            Can be one of the following:
                "join", "begin", "finish"
        @rtype tuple(
                tuple(
                    int: num_customers/throughput,
                    int: total_time,
                    int: min_time,
                    int: max_time,
                    float: mean_time,
                    float: std_time
                ),
                list[int]: list raw time for each customer
            )
            The calculated statistics and raw data.
        """
        
        assert self._finished, "Error; the simulation has not finished running;" \
        + " please run it before generating statistics"
        
        start_time = 0 if start_time is None else start_time
        end_time = float("inf") if end_time is None else end_time
        
        customers = []
        for line in self.store.lines:
            if line_ids is None or line.id in line_ids:
                for customer in line.served:
                    customer_timestamp = None
                    if filter_by == "join":
                        customer_timestamp = customer.join_timestamp
                    elif filter_by == "begin":
                        customer_timestamp = customer.begin_timestamp
                    elif filter_by == "finish":
                        customer_timestamp = customer.finish_timestamp
                    else:
                        raise ValueError("Error: unknown filter_by: %s.", filter_by)
                    if start_time <= customer_timestamp < end_time:
                        customers.append(customer)
        
        raw_time = []
        for customer in customers:
            if criterion == "wait":
                raw_time.append(customer.begin_timestamp - customer.join_timestamp)
            elif criterion == "checkout":
                raw_time.append(customer.finish_timestamp - customer.begin_timestamp)
            elif criterion == "total":
                raw_time.append(customer.finish_timestamp - customer.join_timestamp)
            else:
                raise ValueError("Error: unknown criterion: %s.", criterion)
        
        np_raw_time = np.array(raw_time)
        return ((
            len(customers),
            np_raw_time.sum(),
            np_raw_time.min(),
            np_raw_time.max(),
            np_raw_time.mean(),
            np_raw_time.std()
        ), raw_time)
