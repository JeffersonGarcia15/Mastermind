import pytest
from ..utils.get_hint import get_hint


def test_get_hint_basic():
    secret = "1234"
    guess = "1234"
    assert get_hint(secret, guess) == [4, 0], "All positions and numbers should match"


def test_get_hint_partial_match():
    secret = "1234"
    guess = "1243"
    assert get_hint(secret, guess) == [
        2,
        2,
    ], "Two digits are correct and in the right position, two are correct but wrong position"


def test_get_hint_no_match():
    secret = "1234"
    guess = "5678"
    assert get_hint(secret, guess) == [0, 0], "No digits match"


def test_get_hint_duplicate_digits():
    secret = "1122"
    guess = "2211"
    assert get_hint(secret, guess) == [
        0,
        4,
    ], "All digits match but none are in the correct position"
