from __future__ import annotations

import pytest

from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


class Person:

    def __init__(self, name: Name):
        self.name = name


class Money(NamedTuple):
    currency: str
    value: int

    def __add__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError('Money must have same currency.')

        return Money(
            self.currency,
            self.value + other.value
        )


    def __sub__(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError('Money must have same currency.')

        return Money(
            self.currency,
            self.value - other.value
        )


    def __mul__(self, factor: int) -> Money:
        if type(factor) != int:
            raise TypeError

        return Money(
            self.currency,
            self.value * factor
        )


Line = namedtuple('Line', ['sku', 'qty'])


def test_equality():
    assert Money('gbp', 10) == Money('gbp', 10)
    assert Name('Harry', 'Percival') != Name('Bob', 'Gregory')
    assert Line('CHAIR-1', 5) == Line('CHAIR-1', 5)


# Math with value objects
fiver = Money('gbp', 5)
tenner = Money('gbp', 10)

def test_can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner


def test_can_subtract_money_value():
    assert tenner - fiver == fiver


def test_adding_different_currencies_fails():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('gbp', 10)


def test_can_multiply_money_by_a_number():
    assert fiver * 5 == Money('gbp', 25)


def test_multiplying_two_money_values_is_an_error():
    with pytest.raises(TypeError):
        tenner * fiver


# Testing name and person equality
def test_name_equality():
    assert Name('Harry', 'Percival') != Name('Barry', 'Percival')


def test_barry_is_harry():
    harry = Person(Name('Harry', 'Percival'))
    barry = harry

    barry.name = Name('Barry', 'Percival')

    assert harry is barry and barry is harry
