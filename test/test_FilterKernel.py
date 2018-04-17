import spike
import pytest

def test_gaussian():
    k = spike.kernel('gaussian',sigma=1)
    assert k(0) == 0.3989422804014327
    return
