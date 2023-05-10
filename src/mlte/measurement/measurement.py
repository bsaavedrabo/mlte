"""
Superclass for all measurements.
"""

from __future__ import annotations

import abc
import typing
from typing import Type

from mlte.value import Value
from mlte.evidence import EvidenceMetadata, Identifier


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Measurement(metaclass=abc.ABCMeta):
    """
    The superclass for all model measurements.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete measurements."""
        return all(_has_callable(subclass, method) for method in ["__call__"])

    def __init__(self, instance: Measurement, identifier: str):
        """
        Initialize a new Measurement instance.

        :param instance: The invoking instance (Measurement subclass)
        :type instance: Measurement
        :param identifier: A unique identifier for the instance
        :type identifier: str
        """
        self.metadata = EvidenceMetadata(type(instance).__name__, identifier)
        """The metadata for the measurement instance."""

    @property
    def identifier(self) -> Identifier:
        """Return the measurement identifier."""
        return self.metadata.identifier

    @abc.abstractmethod
    @typing.no_type_check
    def __call__(self, *args, **kwargs) -> Value:
        """Evaluate a measurement and return a value semantics."""
        raise NotImplementedError("Cannot evaluate abstract measurement.")

    @typing.no_type_check
    def evaluate(self, *args, **kwargs) -> Value:
        """
        Evaluate a measurement and return a value with semantics.

        :return: The resulting value of measurement execution, with semantics
        :rtype: Value
        """
        # Evaluate the measurement
        return self.__call__(*args, **kwargs)

    @property
    def value(self) -> Type[Value]:
        """Returns the class type object for the Value produced by the Measurement."""
        raise NotImplementedError(
            "Cannot return Value type for abstract Measurement."
        )

    def __str__(self) -> str:
        """Return a string representation of a Measurement."""
        return f"{self.metadata}"
