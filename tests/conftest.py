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
    return request.param

@pytest.fixture
def shared_fd(dataset_path):
    fd = os.open(dataset_path, os.O_RDONLY)
    yield fd
    os.close(fd)

@pytest.fixture
def csv_reader(dataset_path):
    with open(dataset_path, newline='') as csvfile:
        yield csv.reader(csvfile, delimiter=',')

@pytest.fixture(
    scope="package",
    params=[2, 3, 4, 5, 6, 7, 8]
)
def n_thread(request):
    yield request.param
