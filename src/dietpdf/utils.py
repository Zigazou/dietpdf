"""

"""

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from itertools import combinations
from numpy import prod

def prime_factors_of(num: int) -> list:
    if num < 2:
        return [num]

    factors = []
    factor = 2

    while num > 1:
        if num % factor == 0:
            factors.append(factor)
            num = num // factor
        else:
            factor += 1

    return factors

def multiplications(nums: list) -> list:
    if len(nums) == 1:
        return nums

    mults = set()
    for factor_count in range(1, len(nums)):
        mults |= { prod(tuple) for tuple in combinations(nums, factor_count) }
    return list(mults)

def multiples(num: int) -> list:
    return multiplications(prime_factors_of(num))
