class Customer:
    """A customer object.
    
    Customers are abstracted into objects with simplified attributes.
    A customer has an ID, holds a certain number of grocery items to
    checkout, and knows the time they joins the line, begins checkout,
    and finishes checkout.
    
    === Attributes ===
    @type id: int
        An ID number assigned for this customer.
    @type num_items: int
        Number of grocery items this customer purchases.
    @type join_timestamp:
        The timestamp when the customer joins the checkout line.
    @type begin_timestamp:
        The timestamp when the customer starts checking out.
    @type finish_timestamp:
        The timestamp when the customer finishes checking out.
    """
    
    def __init__(self, id, num_items):
        """Initialize a Customer with an ID and number of grocery items.
        
        @type self: Customer
        @type id: int
            An ID number assigned for this customer.
        @rtype: None
        """
        self.id = id
        self.num_items = num_items
        self.join_timestamp = None
        self.begin_timestamp = None
        self.finish_timestamp = None
