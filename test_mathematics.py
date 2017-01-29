# import pytest
from yMathematics import *


# average
def test_returns_None_instead_of_raising_exceptions():
    assert average([], 0) is None  # empty list
    assert average([], 3) is None  # wrong averaging type
    assert average([[1, 2], 3], 0) is None  # unstructured list
    assert average([[1, 2], [3, 4, 5]], 0) is None  # unstructured list
    assert average([["1", 2], [3, 4]], 0) is None  # wrong data type

def test_for_lists():
    # arithmetic mean
    assert average(2.5, 0) == 2.5  # 0 dim
    assert average([1, 2, 3, 4], 0) == 2.5  # 1 dim
    assert average([[1, 2], [3, 4]], 0) == 2.5  # 2 dim
    assert average([[[1, 2.5], [2, 2.5]], [[3, 3.5], [4, 1.5]]], 0) == 2.5  # 3 dim
    assert average(np.array([1,2,3]), 0) == 2
    # geometic mean
    assert average(2.5, 1) == 2.5  # 0 dim
    assert average([1, 1./32, 4], 1) == 0.5  # 1 dim
    assert average([[2, 8], [2, 8]], 1) == 4  # 2 dim
    assert average([[[2, 8], [2, 8]], [[2, 8], [2, 8]]], 1) == 4  # 3 dim
    assert average(np.array([1, 1./32, 4]), 1) == 0.5

# invert
def test_invert():
    assert invert(1) == 0
    assert invert(0) == 1
    assert invert(True) == False
    assert invert(False) == True