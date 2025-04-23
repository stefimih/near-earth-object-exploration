"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""

import operator
import itertools


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes."""

    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __call__(self, approach):
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


# Subclasses of AttributeFilter
class DateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.time.date()

class StartDateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.time.date()

class EndDateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.time.date()

class DistanceFilterMin(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.distance

class DistanceFilterMax(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.distance

class VelocityFilterMin(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.velocity

class VelocityFilterMax(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.velocity

class DiameterFilterMin(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter

class DiameterFilterMax(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria."""
    filters = []

    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(StartDateFilter(operator.ge, start_date))
    if end_date:
        filters.append(EndDateFilter(operator.le, end_date))
    if distance_min is not None:
        filters.append(DistanceFilterMin(operator.ge, distance_min))
    if distance_max is not None:
        filters.append(DistanceFilterMax(operator.le, distance_max))
    if velocity_min is not None:
        filters.append(VelocityFilterMin(operator.ge, velocity_min))
    if velocity_max is not None:
        filters.append(VelocityFilterMax(operator.le, velocity_max))
    if diameter_min is not None:
        filters.append(DiameterFilterMin(operator.ge, diameter_min))
    if diameter_max is not None:
        filters.append(DiameterFilterMax(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))

    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator."""
    if n is None or n == 0:
        return iterator
    return itertools.islice(iterator, n)

