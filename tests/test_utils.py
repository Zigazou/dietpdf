from random import seed, randrange

from dietpdf.utils import multiplications, multiples, prime_factors_of

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_utils_prime_factors_of():
    assert prime_factors_of(0) == [0]
    assert prime_factors_of(1) == [1]
    assert prime_factors_of(2) == [2]
    assert prime_factors_of(3) == [3]
    assert prime_factors_of(4) == [2, 2]
    assert prime_factors_of(5) == [5]
    assert prime_factors_of(6) == [2, 3]
    assert prime_factors_of(7) == [7]
    assert prime_factors_of(8) == [2, 2, 2]
    assert prime_factors_of(9) == [3, 3]
    assert prime_factors_of(15835) == [5, 3167]

    seed(2022)
    for _ in range(128):
        number = randrange(200000)
        factors = prime_factors_of(number)

        multiplication = factors[0]
        for factor in factors[1:]:
            multiplication *= factor

        assert multiplication == number


def test_utils_multiplications():
    assert multiplications([1]) == [1]
    assert sorted(multiplications([5, 3167])) == [5, 3167]
    assert sorted(multiplications([2, 2, 2, 2])) == [2, 4, 8]


def test_utils_multiples():
    assert multiples(0) == [0]
    assert multiples(1) == [1]
    assert multiples(2) == [2]
    assert multiples(3) == [3]

    seed(2022)
    for _ in range(128):
        number = 1 + randrange(200000)
        mults = multiples(number)

        assert len(mults) >= 1

        for mult in mults:
            assert number % mult == 0
