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
def shared_fd_reader(request):
    p = request.param
    fd = os.open(p, os.O_RDONLY)
    with open(p, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        yield (fd, reader)
        os.close(fd)
