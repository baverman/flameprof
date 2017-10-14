import pytest
import time


@pytest.fixture
def dep(request):
    time.sleep(0.3)
    return None


def test_simple1(dep):
    time.sleep(0.2)


def test_simple2(dep):
    time.sleep(0.2)
