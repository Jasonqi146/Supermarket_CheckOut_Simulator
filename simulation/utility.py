import numpy as np

class Utility:
    """ A class containing useful utility functions.
    
    === Static Attributes ===
    
    @type get_checkout_time: func(Customer, CheckoutLine)
        Get the checkout time given the customer and the line.
        
        The checkout time is a function of the checkout line type and the
        number grocery items the customer purchases.

        The implementation can differ to experiment different settings.
        
    
    @type pick_checkout_line(customer, lines): func(Customer, GroceryStore)
        Pick a checkout line given the customer and checkout lines.
        
        There are several schemes explored for picking a line:
            Pure Random
            Least Person
            Least Item
            Least Time
            Round-Robin
        
        **Bottom rules**:
            cannot pick a closed line.
            can only pick express checkout when having <= 10 items

        The implementation can differ to experiment different settings.
    
    
    @type _checkout_w: dict[str, int]
        weight of linear function to model checkout time
    @type _checkout_b: dict[str, int]
        bias of linear function to model checkout time
    @type count_first: bool
        if count the first customer in a checkout line
        Default True
    """
    
    get_checkout_time = None
    pick_checkout_line = None
    
    _checkout_w = {
        "cashier": 1,
        "express": 1,
        "self":    2
    }
    _checkout_b = {
        "cashier": 7,
        "express": 4,
        "self":    1
    }
    
    count_first = True
    
    @staticmethod
    def get_checkout_time_deterministic(customer, line):
        """Get the checkout time given the customer and the line.

        This implementation assumes the checkout time for each customer is
        deterministic given number of items purchased.

        @type customer: Customer
            The customer to checkout.
        @type line: CheckoutLine
            The checkout line used for checkout.
        @rtype: int
            The time used for checkout.
        """
        if line.type in ("cashier", "express", "self"):
            return customer.num_items * Utility._checkout_w[line.type] + \
        Utility._checkout_b[line.type]
        else:
            raise ValueError("Error: unknown checkout line type:",
                            line.type)
    
    @staticmethod
    def get_checkout_time_stochastic(customer, line):
        """Get the checkout time given the customer and the line.s

        This implementation assumes the checkout time for each customer is
        stochastic (normally distributed) given number of items purchased.

        @type customer: Customer
            The customer to checkout.
        @type line: CheckoutLine
            The checkout line used for checkout.
        @rtype: int
            The time used for checkout.
        """
        # TODO: implement this method.
        
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def pick_checkout_line_least_person(customer, store):
        """Pick a checkout line given the customer and checkout lines.
        
        This is the least person implementation.

        @type customer: Customer
        @type store: GroceryStore
        @rtype: CheckoutLine
            The checkout line to use for checkout.
        """
        best_line = None
        for line in store.lines:
            if not line.closed and (
                line.type != "express" or customer.num_items <= 10) and (
                best_line is None or
                line.get_num_customers() < best_line.get_num_customers()):
                best_line = line
        assert best_line is not None, \
        "Error: to pick a line when all lines are closed/not applicable."
        return best_line
    
    @staticmethod
    def pick_checkout_line_pure_random(customer, store):
        """Pick a checkout line given the customer and checkout lines.
        
        This is the pure random implementation.

        @type customer: Customer
        @type store: GroceryStore
        @rtype: CheckoutLine
            The checkout line to use for checkout.
        """
        lines_avail = []
        for line in store.lines:
            if not line.closed and (
                line.type != "express" or customer.num_items <= 10):
                lines_avail.append(line)
        assert len(lines_avail) != 0, \
        "Error: to pick a line when all lines are closed/not applicable."
        return lines_avail[np.random.randint(len(lines_avail))]
    
    @staticmethod
    def pick_checkout_line_least_item(customer, store):
        """Pick a checkout line given the customer and checkout lines.
        
        This is the least item implementation.

        @type customer: Customer
        @type store: GroceryStore
        @rtype: CheckoutLine
            The checkout line to use for checkout.
        """
        best_line = None
        for line in store.lines:
            if not line.closed and (
                line.type != "express" or customer.num_items <= 10) and (
                best_line is None or
                line.get_num_items() < best_line.get_num_items()):
                best_line = line
        assert best_line is not None, \
        "Error: to pick a line when all lines are closed/not applicable."
        return best_line
    
    @staticmethod
    def pick_checkout_line_least_time(customer, store):
        """Pick a checkout line given the customer and checkout lines.
        
        This is the least time implementation.

        @type customer: Customer
        @type store: GroceryStore
        @rtype: CheckoutLine
            The checkout line to use for checkout.
        """
        best_line = None
        for line in store.lines:
            if not line.closed and (
                line.type != "express" or customer.num_items <= 10) and (
                best_line is None or
                line.get_queue_time(count_first=Utility.count_first) \
                < best_line.get_queue_time(count_first=Utility.count_first)):
                best_line = line
        assert best_line is not None, \
        "Error: to pick a line when all lines are closed/not applicable."
        return best_line
    
    @staticmethod
    def pick_checkout_line_round_robin(customer, store):
        """Pick a checkout line given the customer and checkout lines.
        
        This is the round robin implementation.

        @type customer: Customer
        @type store: GroceryStore
        @rtype: CheckoutLine
            The checkout line to use for checkout.
        """
        next_line = None
        for offset in range(1, store.total_lines+1):
            line_id = (store.last_line_id + offset) % store.total_lines
            line = store.lines[line_id]
            if not line.closed and (
                line.type != "express" or customer.num_items <= 10):
                next_line = line
                break
        assert next_line is not None, \
        "Error: to pick a line when all lines are closed/not applicable."
        store.last_line_id = next_line.id
        return next_line
