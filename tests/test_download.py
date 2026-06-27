"""Integration tests: lacli.main.run output must match the dataset parsed as plain CSV."""
import pytest
from lacli.download.file import download

@pytest.mark.integration
def test_download(shared_fd: int, csv_reader, n_thread: int):
    """Assert `run`'s reconstructed Matrix equals the csv.reader ground truth for each dataset/thread-count combo."""
    matrix = download(shared_fd, n_thread)
    expected = list(csv_reader)

    assert len(matrix.data) == len(expected)
    assert matrix.nums == sum(len(row) for row in expected)
    for actual_row, expected_row in zip(matrix.data, expected):
        assert len(actual_row) == len(expected_row)
        assert actual_row == [float(v) for v in expected_row]
