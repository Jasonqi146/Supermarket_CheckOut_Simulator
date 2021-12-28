from .checkout_line import CheckoutLine

class GroceryStore:
    """A grocery store.

    A grocery store contains different types of checkout lines.

    === Attributes ===
    @type lines: list[CheckoutLine]
        A list of checkout lines.
    @type last_line_id: int
        The last line picked by a customer to checkout.
        Particularly useful for round-robin assignment scheme.
    @type total_lines: int
        The number of checkout lines in total.
    """
    
    def __init__(self, line_counts):
        """Initialize a GroceryStore given number of each type of line.

        @type line_counts: dict[str, int]
            A mapping from each checkout line type to how many there are.
            Contains the follwing keys:
                "cashier_count", "express_count", "self_count"
        @rtype: None
        """
        self.lines = []
        line_id = 0
        for line_type, line_count in sorted(line_counts.items()):
            for _ in range(line_count):
                self.lines.append(CheckoutLine(line_id, line_type))
                line_id += 1
        self.last_line_id = line_id - 1
        self.total_lines = line_id
