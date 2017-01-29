from functools import reduce
import numpy as np


def average(_list, average_type):
    """
    average of list or numpy array elements
    list / array can have arbitrary dimension, but must be structured
    :param _list: list of ints, floats or numpy array
    :param averageType: 0: arithmetic, 1: geometric
    :return: average or None instead of raising exceptions
    """
    result = None
    a = np.array(_list)
    a = a.reshape(a.size)  # then it's 1-dim

    if average_type == 0:  # arithmetic
        try:
            result = reduce(lambda x, y: x+y, a) / a.size
        except:  # to capture empty list
            pass
    elif average_type == 1:  # geometric
        try:
            result = reduce(lambda x, y: x*y, a) ** (1. / a.size)
        except:  # to capture empty list
            pass
    else:
        print("Error: Average type must be 0 or 1")

    if not isinstance(result, list):  # reduce gives list for cases like [[1,2],[3]]
        return result

    return None  # e.g. for  [[1,2],3], average_type = 3


def invert(value):
    return 1 if not value else 0

