import numpy as np

class DataGenerator:
    """A data generator to random virtual simulation data.
    
    === Attributes ===
    @type random_state: int
        An optional random seed used to genearte fixed data for benchmarking.
    """
    
    def __init__(self, random_state=None):
        """Initialize a data generator given an optional random seed.
        
        @type self: DataGenerator
        @type random_state: int
            A random state seed.
        @rtype: None
        """
        self.random_state = random_state
    
    def _generate_uniform_time(self, start_time, end_time, num_customers,
                               item_distribution="uniform", *dist_params):
        """Generate time uniformally-distributed virtual customer data.
        
        @type self: DataGenerator
        @type start_time: int
            Start timestamp, inclusive
        @type end_time: int
            End timestamp, exclusive
        @type num_customers: int
            Number of customers to generate.
        @type item_distribution: str
            Distribution to sample in for number of items.
            "uniform" or "gaussian"
        @type dist_params: list[int], len=2
            Two parameters used for a type of distribution.
            For "uniform", they are min and max
            For "gaussian", they are mean and std
        @rtype str: line-separated string to represent a list of initial events.
        """
        assert item_distribution in ("uniform", "gaussian"), \
        "Error: unknown item distribution type: %s." %item_distribution
        assert len(dist_params) == 2, "Error: incorrect number of parameters given."
        
        timestamps = sorted(list(np.floor(np.random.uniform(
            start_time, end_time, num_customers)).astype(int)))
        
        if item_distribution == "uniform":
            sampling_func = np.random.uniform
        else:
            sampling_func = np.random.normal
        
        param1, param2 = dist_params
        items = np.round(sampling_func(param1, param2, num_customers)).astype(int)
        items[items <= 0] = 1 # at least 1 item purchased
        items = list(items)
        
        lines = []
        for timestamp, item in zip(timestamps, items):
            lines.append("%d,join,%d" % (timestamp, item))
        
        return lines
    
    def generate_time_varying(self, params):
        """Generate time-varying data distribution of customer arrival events.
        
        @type self: DataGenerator
        @type params: list[
            tuple(
                int: start_time,
                int: end_time,
                int: num_customers,
                str: item_distribution,
                float: param1 for distribution,
                float: param2 for distribution
            )]
            Time-varying data distribution can be approximated by a list of uniformly
            sampled intervals. In this list, each element is a parameterized tuple.
        @rtype str: line-separated string to represent a list of initial events.
        """
        if self.random_state is not None:
            np.random.seed(self.random_state)
        lines = []
        for sub_params in params:
            lines += self._generate_uniform_time(*sub_params)
        return "\n".join(lines)
