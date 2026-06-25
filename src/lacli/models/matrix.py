"""Data structures shared between the load and reconstruction stages."""

class ChunkMetadata:
    """Parsed output of a single file chunk: extracted numbers and boundary flags used during merge."""
    def __init__(self):
        self.newline_num = 0
        self.is_first_stop = False   # True if the chunk starts with '\n' (no leading truncated token)
        self.is_last_truncated = False  # True if the last token was cut at the chunk boundary
        self.data: list[str] = []

class Matrix:
    """
    The reconstructed numeric grid: `data` is a list of rows, each a list of numbers
    (strings until converted to float by `reconstruct`). `rows`/`cols`/`nums` are
    counts derived during reconstruction.
    """
    def __init__(self):
        self.cols = 0
        self.rows = 0
        self.nums = 0
        self.data = []
