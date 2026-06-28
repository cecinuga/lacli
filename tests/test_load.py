"""Integration tests: lacon.main.run output must match the dataset parsed as plain CSV."""
import numpy as np
import pytest
from lacon.main import run

@pytest.mark.integration
def test_load(dataset_path, csv_reader):
    """Assert `run`'s numpy matrix equals the csv.reader ground truth for each dataset/thread-count combo."""
    matrix = run(dataset_path)
    expected = np.array([[float(v) for v in row] for row in csv_reader])

    assert matrix.shape == expected.shape
    np.testing.assert_allclose(matrix, expected)
