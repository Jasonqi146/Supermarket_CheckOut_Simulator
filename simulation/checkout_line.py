from queue import Queue
from functools import reduce
from .utility import Utility

class CheckoutLine:
    """A checkout line object.
    
    A checkout line has an id, a type attribute, and a queue where
    customers wait for checkout.
    
    === Attributes ===
    @type id: int
        An ID number assigned for this checkout line.
    @type type: string
        The type of this checkout line. Can be one of the following:
            "cashier", "express", "self"
    @type queue: Queue[Customer]
        A first-come-first-serve (FCFS) queue where customers wait.
    @type served: list[Customers]
        A list of previously served customers.
    @type closed: bool
        A boolean to indicate if the checkout line is closed.
        If a line is closed, no new customers can join this line.
    """
    
    def __init__(self, id, type, closed=False):
        """Initialize a CheckoutLine with an ID and a type.
        
        @type self: CheckoutLine
        @type id: int
            An ID number assigned for this checkout line.
        @type type: string
            The type of this checkout line. Must be one of "cashier",
            "express", and "self"
        @type closed: bool
            If the line is closed. Default False.
        @rtype: None
        """
        self.id = id
        self.type = type
        self.queue = Queue()
        self.served = []
        self.closed = closed
        
    def serve_next_customer(self):
        """Serve the next customer.
        
        Do not remove the customer from the queue.
        Instead, remove the customer in FinishCheckoutEvent.
        
        @type self: CheckoutLine
        @rtype: Customer
            The customer to server, in the front of the queue.
        """
        assert not self.is_empty(), "Error: cannot serve next customer from"  \
        + " empty queue of line id: " + str(self.id) + "."
        return self.queue.queue[0]
    
    def queue_new_customer(self, customer):
        """Join a new customer to wait in the queue.
        
        @type self: CheckoutLine
        @type customer: Customer
            The new customer to add to wait in the queue.
        @rtype: None
        """
        assert not self.closed, "Error: cannot accpet new customer in closed" \
        + " line id: " + str(self.id) + "."
        self.queue.put(customer)
    
    def get_num_customers(self):
        """Get the number of customers in the line.
        
        @type self: CheckoutLine
        @rtype: int
            The number of customers in this line.
        """
        return self.queue.qsize()
    
    def is_empty(self):
        """Get if the line has no customer waiting in the queue.
        
        @type self: CheckoutLine
        @rtype: bool
            If the line is empty.
        """
        return self.get_num_customers() == 0
    
    def get_num_items(self):
        """Get the number of items purchased by the customers waiting
        in this line.
        
        @type self: CheckoutLine
        @rtype: int
            The number of items in this line.
        """
        return reduce(
            lambda accum, customer: accum + customer.num_items,
            self.queue.queue, 0)
    
    def get_queue_time(self, count_first=True):
        """Get the expected time to wait in queue if a new customer joins.
        
        @type self: CheckoutLine
        @type count_first: bool
            If count the checkout time of the current customer.
            Default True.
        @rtype: int
            The expected queueing time in this line.
        """
        customers = self.queue.queue
        if len(customers) == 0:
            return 0
        wait_time = 0
        start_idx = 0 if count_first else 1
        for idx in range(start_idx, len(customers)):
            wait_time += Utility.get_checkout_time(customers[idx], self)
        return wait_time
    
    def close(self):
        """Close the line, so no new customers can join.
        
        @type self: CheckoutLine
        @rtype: None
        """
        self.closed = True
    
    def open(self):
        """Open the line, so new customers can join.
        
        @type self: CheckoutLine
        @rtype: None
        """
        self.closed = False
