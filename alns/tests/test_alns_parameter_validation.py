import numpy.random as rnd
from numpy.testing import assert_raises

from alns import ALNS
from .states import One, Zero

state = rnd.RandomState(0)


def test_raises_missing_destroy_operator():
    """
    Tests if the algorithm raises when no destroy operators have been set.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], 0.95)


def test_raises_missing_repair_operator():
    """
    Tests if the algorithm raises when no repair operators have been set.
    """
    alns = ALNS()

    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], 0.95)


def test_raises_negative_operator_decay():
    """
    Tests if the algorithm raises when a negative operator decay parameter is
    passed.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], -0.5)


def test_raises_explosive_operator_decay():
    """
    Tests if the algorithm raises when an explosive operator decay parameter is
    passed.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], 1.2)


def test_raises_boundary_operator_decay():
    """
    The boundary cases, zero and one, should both raise.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], 0)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], 1)


def test_raises_insufficient_weights():
    """
    We need (at least) four weights to be passed-in, one for each updating
    scenario.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1], .5)


def test_raises_non_positive_weights():
    """
    The passed-in weights should all be strictly positive.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 0, 1], .5)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, -5, 1], .5)


def test_raises_non_positive_iterations():
    """
    The number of iterations should be strictly positive.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], .5, 0)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], .5, -5)


def test_raises_negative_temperature_decay_parameter():
    """
    A negative decay parameter would result in a negative temperature, which
    should not be allowed.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], .5, temperature_decay=-0.5)


def test_raises_explosive_temperature_decay_parameter():
    """
    Temperatures would increase without bound for a decay parameter greater
    than one, so this should raise.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], .5, temperature_decay=2.5)


def test_raises_boundary_temperature_decay_parameters():
    """
    The boundary cases, zero and one, should both raise.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: None)
    alns.add_destroy_operator(lambda state, rnd: None)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], .5, temperature_decay=0)

    with assert_raises(ValueError):
        alns.iterate(One(), [1, 1, 1, 1], .5, temperature_decay=1)


def test_does_not_raise():
    """
    This set of parameters, on the other hand, should work correctly.
    """
    alns = ALNS()

    alns.add_repair_operator(lambda state, rnd: One())
    alns.add_destroy_operator(lambda state, rnd: One())

    alns.iterate(Zero(), [1, 1, 1, 1], .5, 100)