"""
test/value/types/test_integer.py

Unit tests for Integer.
"""

import pytest

from mlte.evidence.identifier import Identifier
from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement import Measurement
from mlte.value.types import Integer


class DummyMeasurementInteger(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self) -> Integer:
        return Integer(self.metadata, 1)


def test_integer_success():
    # Ensure instantiation succeeds for valid type
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Integer(m, 1)
    assert i.value == 1


def test_integer_fail():
    # Ensure instantiation fails for invalid type
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    with pytest.raises(AssertionError):
        _ = Integer(m, 3.14)  # type: ignore


def test_integer_serde():
    # Ensure serialization and deserialization are inverses
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Integer(m, 1)

    serialized = i.serialize()
    recovered = Integer.deserialize(m, serialized)
    assert recovered == i


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_integer_save_load(tmp_path):
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    i = Integer(m, 1)

    # Save
    i.save()

    # Recover
    r = Integer.load("id")

    assert r == i


def test_integer_e2e():
    m = DummyMeasurementInteger("identifier")
    i = m.evaluate()
    assert isinstance(i, Integer)
    assert i.value == 1
