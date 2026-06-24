import pytest
from lacli.main import run

@pytest.mark.integration
def test_lacli(shared_fd_reader):
    fd, reader = shared_fd_reader
    print(shared_fd_reader)
