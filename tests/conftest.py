"""Shared pytest fixtures: parametrizes tests over every dataset file and several thread counts."""
import csv
from pathlib import Path
import os
import pytest

DATASET_DIR = Path(__file__).parent / "datasets"

@pytest.fixture(
    scope="package",
    params=sorted(DATASET_DIR.glob("*")),
    ids=lambda p: p.name,
)
def dataset_path(request):
    """Return each dataset file path under tests/datasets, one per parametrized test run."""
    return request.param

@pytest.fixture
def shared_fd(dataset_path):
    """Open `dataset_path` read-only and yield its file descriptor, closing it after the test."""
    fd = os.open(dataset_path, os.O_RDONLY)
    yield fd
    os.close(fd)

@pytest.fixture
def csv_reader(dataset_path):
    """Yield a csv.reader over `dataset_path`, used as the ground truth to compare against."""
    with open(dataset_path, newline='') as csvfile:
        yield csv.reader(csvfile, delimiter=',')

@pytest.fixture(
    scope="package",
    params=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
)
def n_thread(request):
    """Yield each candidate worker-thread count to exercise varying levels of parallelism."""
    yield request.param
