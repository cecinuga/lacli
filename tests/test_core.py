import pytest
from lacli.main import run

@pytest.mark.integration
def test_lacli(shared_fd, csv_reader, n_thread):
    matrix = run(shared_fd, n_thread)
    expected = list(csv_reader)
    assert len(matrix.data) == len(expected)
    for actual_row, expected_row in zip(matrix.data, expected):
        assert len(actual_row) == len(expected_row)
        assert actual_row == [float(v) for v in expected_row]
