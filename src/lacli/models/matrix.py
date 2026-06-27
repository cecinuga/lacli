"""Data structures shared between the load and reconstruction stages."""

class Matrix:
    """
    The reconstructed numeric grid: `data` is a list of rows, each a list of numbers
    (strings until converted to float). `rows`/`cols`/`nums` are derived counts.
    """
    def __init__(self):
        self.cols = 0
        self.rows = 0
        self.nums = 0
        self.data = []
