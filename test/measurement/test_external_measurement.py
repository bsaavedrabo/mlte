"""
test/measurement/test_external_measurement.py

Unit test for ExternalMeasurement.
"""

import pytest

from mlte.evidence.identifier import Identifier
from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement import ExternalMeasurement
from mlte.value.types.integer import Integer


def _dummy_calculation(x: int, y: int):
    """
    Dummy calculation function that adds two ints and multiplies the result by two.

    :param x: The first number
    :type x: int
    :param y: The second number
    :type y: int

    :return: the result of the calculation
    :rtype: int
    """
    return (x + y) * 2


def test_evaluate_external():
    x = 1
    y = 2
    expected_value = _dummy_calculation(x, y)
    expected_result = Integer(
        EvidenceMetadata(
            measurement_type="dummy", identifier=Identifier(name="test")
        ),
        expected_value,
    )

    measurement = ExternalMeasurement("dummy", Integer, _dummy_calculation)
    result = measurement.evaluate(x, y)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_evaluate_ingest():
    expected_value = 1000
    expected_result = Integer(
        EvidenceMetadata(
            measurement_type="dummy", identifier=Identifier(name="test")
        ),
        expected_value,
    )

    measurement = ExternalMeasurement("dummy", Integer)
    result = measurement.ingest(expected_value)

    assert isinstance(result, Integer)
    assert result == expected_result


def test_invalid_result_type():
    with pytest.raises(Exception):
        ExternalMeasurement("dummy", int)


def test_invalid_function():
    with pytest.raises(Exception):
        ExternalMeasurement("dummy", Integer, "not_a_function")


def test_evaluate_no_function():
    x = 1
    y = 2

    measurement = ExternalMeasurement("dummy", Integer)
    with pytest.raises(Exception):
        measurement.evaluate(x, y)
