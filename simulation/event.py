from .utility import Utility
from .customer import Customer

class Event:
    
    """A generic event.

    Events are organized in non-ascending order based on their timestamps.
    Subclasses of Event must implement do() because this class is abstract.

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    @type customer: Customer
        The customer associated with this event, nullable.
        This field is set when the follwing events are assigned.
            JoinCheckoutEvent
            BeginCheckoutEvent
            FinishCheckoutEvent
    @type line: CheckoutLine
        The line associated with this event, nullable.
        This field is set when the follwing events are assigned.
            JoinCheckoutEvent
            BeginCheckoutEvent
            FinishCheckoutEvent
            LineCloseEvent
            LineOpenEvent
    """
    
    def __init__(self, timestamp, customer=None, line=None):
        """Initialize an Event with a given timestamp, customer, and line.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
        @type customer: Customer
            The customer associated with this event.
        @type line: CheckoutLine
            The line associated with this event.
        @rtype: None
        """
        self.timestamp = timestamp
        self.customer = customer
        self.line = line

    def __eq__(self, other):
        return self.timestamp == other.timestamp
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    
    def __le__(self, other):
        return self.timestamp <= other.timestamp
    
    def __gt__(self, other):
        return not self.__le__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)
    
    def do(self, store):
        """Perform this Event.

        Call methods on <store> to update its state according to the
        meaning of the event.
        
        Return a list of new events spawned by this event with correct
        timestamps.

        @type self: Event
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        # There is no need to implement this because Event is abstract.
        # subclasses of Event will have to implement it.
        raise NotImplementedError


class BeginCheckoutEvent(Event):
    
    """The event to begin checkout process.

    This event is generated when a new customer joins an empty checkout
    line or when another customer in front of them finishes checkout.

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    @type customer: Customer
        The customer associated with this event.
    @type line: CheckoutLine
        The line associated with this event.
    """
    
    def do(self, store):
        """Perform this Event.
        
        Once the customer begins checkout, a new FinishCheckoutEvent is
        then generated with the updated timestamp to reflect when the
        customer finishes checkout.
        
        @type self: BeginCheckoutEvent
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        self.customer.begin_timestamp = self.timestamp
        checkout_time = Utility.get_checkout_time(self.customer, self.line)
        return [FinishCheckoutEvent(
            self.timestamp + checkout_time, self.customer, self.line)]

    
class FinishCheckoutEvent(Event):
    
    """The event to finish checkout process.

    This event is generated when a new customer begins checkout.

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    @type customer: Customer
        The customer associated with this event.
    @type line: CheckoutLine
        The line associated with this event.
    """
    
    def do(self, store):
        """Perform this Event.
        
        Once the customer finishes checkout, if the checkout line still
        has customers waiting in the queue, the next customer is removed
        from the queue, and a BeginCheckoutEvent is assigned for them
        with the same timestamp this customer finishes checkout.
        Otherwise, do nothing (empty list returned).
        
        @type self: FinishCheckoutEvent
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        self.customer.finish_timestamp = self.timestamp
        served_customer = self.line.queue.get()
        self.line.served.append(served_customer)
        if not self.line.is_empty():
            next_customer = self.line.serve_next_customer()
            return [BeginCheckoutEvent(
                self.timestamp, next_customer, self.line)]
        else:
            return []


class JoinCheckoutEvent(Event):
    
    """The event to allow a customer to prepare for checkout.
    
    This event is generated when a new customer joins checkout zone.

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    @type customer: Customer
        The customer associated with this event.
    """
    
    def __init__(self, timestamp, customer):
        """Initialize an Event with a given timestamp and customer.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
        @type customer: Customer
            The customer associated with this event.
        @rtype: None
        """
        super().__init__(timestamp, customer=customer, line=None)
    
    def do(self, store):
        """Perform this Event.
        
        Once the customer joins, a checkout line is then picked.
        The customer is added to the checkout line queue.
        If the picked line is empty, a BeginCheckoutEvent will also be
        generated for this customer with the same timestamp as this event.
        
        @type self: JoinCheckoutEvent
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        self.customer.join_timestamp = self.timestamp
        self.line = Utility.pick_checkout_line(self.customer, store)
        if self.line.is_empty():
            # IMPORTANT: do not try to remove/simplify the following line
            self.line.queue_new_customer(self.customer)
            return [BeginCheckoutEvent(
                self.timestamp, self.customer, self.line)]
        else:
            self.line.queue_new_customer(self.customer)
            return []


class LineOpenEvent(Event):
    """The event to open a checkout line.
    
    This event is generated when a line is about to open.

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    @type line: CheckoutLine
        The line associated with this event.
    """
    
    def __init__(self, timestamp, line):
        """Initialize an Event with a given timestamp and line.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
        @type line: CheckoutLine
            The line associated with this event.
        @rtype: None
        """
        super().__init__(timestamp, customer=None, line=line)
    
    def do(self, store):
        """Perform this Event.
        
        Open the line.
        
        @type self: LineOpenEvent
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        self.line.open()
        return []


class LineCloseEvent(Event):
    """The event to close a checkout line.
    
    This event is generated when a line is about to close.

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    @type line: CheckoutLine
        The line associated with this event.
    """
    
    def __init__(self, timestamp, line):
        """Initialize an Event with a given timestamp and line.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
        @type line: CheckoutLine
            The line associated with this event.
        @rtype: None
        """
        super().__init__(timestamp, customer=None, line=line)
    
    def do(self, store):
        """Perform this Event.
        
        Close the line.
        
        @type self: LineCloseEvent
        @type store: GroceryStore
        @rtype: list[Event]
            A list of events generated by performing this event.
        """
        self.line.close()            
        return []


def create_event_list(initial_events_str, store):
    """Return a list of Events based on raw str list of events.

    @type initial_events_str: str
        A line-separated string to represent a list of initial events.
        Sample format of each line:
            <timestamp>, join, <num_items>         <- customer joins
            <timestamp>, open, <line_id>           <- line opens
            <timestamp>, close, <line_id>          <- line closes
    @type stroe: GroceryStore
        The grovery store associated with the simulation.
    @rtype: list[Event]
         A list of initial events.
    """
    events = []
    curr_customer_id = 0
    for idx, line in enumerate(initial_events_str.strip().split("\n")):
        try:
            timestamp, event_type, param = line.split(",")
            timestamp, param = int(timestamp), int(param)
            if event_type == "join":
                customer = Customer(curr_customer_id, param)
                curr_customer_id += 1
                event = JoinCheckoutEvent(timestamp, customer)
            elif event_type in ("open", "close"):
                line = list(filter(lambda line: line.id == param,
                              store.lines))[0]
                if event_type == "open":
                    event = LineOpenEvent(timestamp, line)
                else:
                    event = LineCloseEvent(timestamp, line)
            else:
                raise ValueError("Error: unknown event type '%s'."
                                 % event_type)
        except:
            raise ValueError("Error: parse error on line %d." % idx)
        events.append(event)
    return events
