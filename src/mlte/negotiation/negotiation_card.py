"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel

from mlte.artifact import Artifact, ArtifactType
from mlte.context import Context
from mlte.session import session_state


class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        *,
        context: Context,
        identifier: str,
        system: SystemDescriptor,
        data: list[DataDescriptor],
        model: ModelDescriptor,
    ) -> None:
        super().__init__(context, ArtifactType.NEGOTIATION_CARD, identifier)

        self.system = system
        """A description of the system into which the model is integrated."""

        self.data = data
        """A description of the dataset(s) used to train the model."""

        self.model = model
        """A description of the model itself."""

    @staticmethod
    def new(
        identifier: str,
        system: SystemDescriptor,
        data: list[DataDescriptor],
        model: ModelDescriptor,
    ) -> NegotiationCard:
        """
        Factory method to produce a new negotiation card in the session context.
        :param identifier: An identifier for the artifact
        :param system: The system descriptor
        :param data: A collection of data descriptors
        :param model: The model descriptor
        :return The negotiation card instance
        """
        return NegotiationCard(
            context=session_state().context,
            identifier=identifier,
            system=system,
            data=data,
            model=model,
        )

    @staticmethod
    def in_context(
        context: Context,
        identifier: str,
        system: SystemDescriptor,
        data: list[DataDescriptor],
        model: ModelDescriptor,
    ) -> NegotiationCard:
        """
        Factory method to produce a new negotiation card in a specified context.
        :param context: The context in which the negotiation card is constructed
        :param identifier: An identifier for the artifact
        :param system: The system descriptor
        :param data: A collection of data descriptors
        :param model: The model descriptor
        :return: The negotiation card instance
        """
        return NegotiationCard(
            context=context,
            identifier=identifier,
            system=system,
            data=data,
            model=model,
        )

    def to_json(self) -> dict[str, Any]:
        """
        Serialize a negotiation card artifact to JSON document.
        :return: The serialized document
        """
        return {}

    @staticmethod
    def from_json(document: dict[str, Any]) -> NegotiationCard:
        """
        Deserialize a negotiation card artifact from JSON document.
        :param document: The input document
        :return: The deserialized negotiation card artifact
        """


# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


class SystemDescriptor(BaseModel):
    """A description of the system context."""

    goals: list[GoalDescriptor]
    """A description of system goals."""

    problem_type: ProblemType
    """A description of the machine learning problem type."""

    task: str
    """A description of the machine learning task."""

    usage_context: str
    """A description of the usage context."""

    risks: RiskDescriptor
    """A description of risks associated with system failures."""


class ProblemType(Enum):
    """An enumeration over machine learning problem types."""

    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"
    TREND = "trend"
    ALERT = "alert"
    FORECASTING = "forecasting"
    CONTENT_GENERATION = "content_generation"
    BENCHMARKING = "benchmarking"
    GOALS = "goals"
    DETECTION = "detection"
    OTHER = "other"


class GoalDescriptor(BaseModel):
    """A description of a system goal."""

    description: str
    """A description of the goal."""

    metrics: list[MetricDescriptor]
    """A collection of metrics related to the goal."""


class MetricDescriptor(BaseModel):
    """A description of a metric that supports a system goal."""

    description: str
    """A description of the metric."""

    baseline: str
    """A description of the metric baseline value."""


class RiskDescriptor(BaseModel):
    """A description of system-level risks."""

    fp: str
    """A description of risks associated with false-positives."""

    fn: str
    """A description of risks associated with false-negatives."""

    other: str
    """A description of risks associated with other failures."""


# -----------------------------------------------------------------------------
# Data Subcomponents
# -----------------------------------------------------------------------------


class DataDescriptor(BaseModel):
    """Describes a dataset used in model development."""

    description: str
    """A description of the dataset."""

    source: str
    """A description of the data source."""

    classification: DataClassification
    """A description of the data classification level."""

    access: str
    """A description of the manner in which this data is accessed."""

    labels: list[DataLabelDescriptor]
    """A description of the labels that appear in the dataset."""

    fields: list[DataFieldDescriptor]
    """A description of the dataset schema."""

    rights: str
    """A description of the ways in which the data can / cannot be used."""

    policies: str
    """A description of the policies that govern use of this data."""

    identifiable_information: str
    """A description of personaly-identifiable information considerations for this dataset."""


class DataClassification(Enum):
    """An enumeration of data classification levels."""

    UNCLASSIFIED = "unclassified"
    CUI = "cui"
    PII = "pii"
    PHI = "phi"
    OTHER = "other"


class DataLabelDescriptor(BaseModel):
    """Describes a dataset label."""

    description: str
    """A description of the label."""

    percentage: float
    """The relative frequency with which the label occurs in the dataset."""


class DataFieldDescriptor(BaseModel):
    """Describes a dataset field."""

    name: str
    """The name of the field."""

    description: str
    """A description of the field."""

    type: str
    """A description of the field type."""

    expected_values: str
    """An example of expected values for the field."""

    missing_values: str
    """An example of missing values for the field."""

    special_values: str
    """An example of special values for the field."""


# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


class ModelDescriptor(BaseModel):
    """A descriptor for the model."""


class ModelDevelopmentDescriptor(BaseModel):
    """A descriptor for model development considerations."""

    resources: ModelResourcesDescriptor
    """A description of model development resource requirements."""


class ModelProductionDescriptor(BaseModel):
    """A descriptor for model production considerations."""

    integration: str
    """A description of the manner in which the model is integrated with the system."""

    interface: ModelInterfaceDescriptor
    """A description of the model interface."""

    resources: ModelResourcesDescriptor
    """A description of model production resource requirements."""


class ModelResourcesDescriptor(BaseModel):
    """A descriptor for model resource requirements."""

    cpu: str
    """A description of model CPU requirements."""

    gpu: str
    """A description of model GPU requirements."""

    memory: str
    """A description of model memory (RAM) requirements."""

    storage: str
    """A description of model storage requirements."""


class ModelInterfaceDescriptor(BaseModel):
    """A description of the model interface."""

    input: ModelInputDescriptor
    """The model input specification."""

    output: ModelOutputDescriptor
    """The model output specification."""


class ModelInputDescriptor(BaseModel):
    """A description of the model input specification."""

    description: str
    """A textual description of the input specification."""


class ModelOutputDescriptor(BaseModel):
    """A description of the model output specification."""

    description: str
    """A textual description of the output specification."""
