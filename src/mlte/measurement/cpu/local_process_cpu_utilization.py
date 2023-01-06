"""
CPU utilization measurement for local training processes.
"""

from __future__ import annotations

import time
import subprocess
from typing import Dict, Any
from subprocess import SubprocessError

from mlte.measurement import Measurement, MeasurementMetadata
from mlte.measurement.result import Result
from mlte.measurement.validation import (
    Validator,
    ValidationResult,
    Success,
    Failure,
)
from mlte._private.platform import is_windows

# -----------------------------------------------------------------------------
# CPUStatistics
# -----------------------------------------------------------------------------


class CPUStatistics(Result):
    """
    The CPUStatistics class encapsulates data
    and functionality for tracking and updating
    CPU consumption statistics for a running process.
    """

    def __init__(
        self,
        measurement_metadata: MeasurementMetadata,
        avg: float,
        min: float,
        max: float,
    ):
        """
        Initialize a CPUStatistics instance.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement_metadata: MeasurementMetadata
        :param avg: The average utilization
        :type avg: float
        :param min: The minimum utilization
        :type min: float
        :param max: The maximum utilization
        :type max: float
        """
        super().__init__(self, measurement_metadata)

        self.avg = avg
        """The average CPU utilization, as a proportion."""

        self.min = min
        """The minimum CPU utilization, as a proportion."""

        self.max = max
        """The maximum CPU utilization, as a proportion."""

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize an CPUStatistics to a JSON object.

        :return: The JSON object
        :rtype: Dict[str, Any]
        """
        return {"avg": self.avg, "min": self.min, "max": self.max}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> CPUStatistics:
        """
        Deserialize an CPUStatistics from a JSON object.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement_metadata: MeasurementMetadata
        :param json: The JSON object
        :type json: Dict[str, Any]

        :return: The deserialized instance
        :rtype: Integer
        """
        return CPUStatistics(
            measurement_metadata,
            avg=json["avg"],
            min=json["min"],
            max=json["max"],
        )

    def __str__(self) -> str:
        """Return a string representation of CPUStatistics."""
        s = ""
        s += f"Average: {self.avg:.2f}%\n"
        s += f"Minimum: {self.min:.2f}%\n"
        s += f"Maximum: {self.max:.2f}%"
        return s

    def max_utilization_less_than(self, threshold: float) -> ValidationResult:
        """
        Construct and invoke a validator for maximum CPU utilization.

        :param threshold: The threshold value for maximum utilization
        :type threshold: float

        :return: The validation result
        :rtype: ValidationResult
        """
        return Validator(
            "MaximumUtilization",
            lambda stats: Success(
                f"Maximum utilization {stats.max:.2f} "
                f"below threshold {threshold:.2f}"
            )
            if stats.max < threshold
            else Failure(
                (
                    f"Maximum utilization {stats.max:.2f} "
                    f"exceeds threshold {threshold:.2f}"
                )
            ),
        )(self)

    def average_utilization_less_than(
        self, threshold: float
    ) -> ValidationResult:
        """
        Construct and invoke a validator for average CPU utilization.

        :param threshold: The threshold value for average utilization
        :type threshold: float

        :return: The validation result
        :rtype: ValidationResult
        """
        return Validator(
            "AverageUtilization",
            lambda stats: Success(
                f"Average utilization {stats.max:.2f} "
                f"below threshold {threshold:.2f}"
            )
            if stats.avg < threshold
            else Failure(
                (
                    f"Average utilization {stats.avg:.2f} "
                    "exceeds threshold {threshold:.2f}"
                )
            ),
        )


# -----------------------------------------------------------------------------
# LocalProcessCPUUtilization
# -----------------------------------------------------------------------------


class LocalProcessCPUUtilization(Measurement):
    """Measures CPU utilization for a local process."""

    def __init__(self, identifier: str):
        """
        Initialize a new LocalProcessCPUUtilization measurement.

        :param identifier: A unique identifier for the measurement
        :type identifier: str
        """
        super().__init__(self, identifier)
        if is_windows():
            raise RuntimeError(
                f"Measurement {self.name} is not supported on Windows."
            )

    def __call__(self, pid: int, poll_interval: int = 1) -> CPUStatistics:
        """
        Monitor the CPU utilization of process at `pid` until exit.

        :param pid: The process identifier
        :type pid: int
        :param poll_interval: The poll interval in seconds
        :type poll_interval: int

        :return: The collection of CPU usage statistics
        :rtype: Dict
        """
        stats = []
        while True:
            util = _get_cpu_usage(pid)
            if util < 0.0:
                break
            stats.append(util / 100.0)
            time.sleep(poll_interval)

        return CPUStatistics(
            self.metadata,
            avg=sum(stats) / len(stats),
            min=min(stats),
            max=max(stats),
        )


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_cpu_usage(pid: int) -> float:
    """
    Get the current CPU usage for the process with `pid`.

    :param pid: The identifier of the process
    :type pid: int

    :return: The current CPU utilization as percentage
    :rtype: float
    """
    try:
        stdout = subprocess.check_output(
            ["ps", "-p", f"{pid}", "-o", "%cpu"], stderr=subprocess.DEVNULL
        ).decode("utf-8")
        return float(stdout.strip().split("\n")[1].strip())
    except SubprocessError:
        return -1.0
    except ValueError:
        return -1.0
