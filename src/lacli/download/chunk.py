class ChunkMetadata:
    """Parsed output of a single file chunk: extracted numbers and boundary flags used during merge."""
    def __init__(self):
        self.newline_num = 0
        self.is_first_stop = False   # True if the chunk's first byte is a delimiter ('\n' or ','), i.e. no leading truncated token
        self.is_last_truncated = False  # True if the last token was cut at the chunk boundary
        self.data: list[str] = []
