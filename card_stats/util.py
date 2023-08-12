from functools import reduce
from typing import Dict, Sequence, Union


def reduce_sum(iterable: Union[Dict, Sequence]) -> Union[int, float]:
    if isinstance(iterable, dict):
        iterable = list(iterable.values())
    print(iterable)
    try:
        return reduce(lambda a, b: a + b, iterable, 0)
    except:
        raise ValueError("Could not sum up iterable {}".format(iterable))
