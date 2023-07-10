"""
Data model implementation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResultVersion:
    """Represents an individual value version."""

    # The version identifier
    version: int
    # The value payload
    data: Dict[str, Any]

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        return {"version": self.version, "data": self.data}

    @staticmethod
    def from_json(json: Dict[str, Any]):
        """Deserialize from JSON object."""
        assert all(
            n in json for n in ["version", "data"]
        ), "Broken precondition."
        return ResultVersion(version=json["version"], data=json["data"])


@dataclass
class Value:
    """Represents an individual value (a collection of versions)."""

    # The identifier for the value
    identifier: str
    # The tag associated with the value
    tag: Optional[str] = None
    # A collection of value versions
    versions: List[ResultVersion] = field(default_factory=lambda: [])

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON object."""
        return {
            "identifier": self.identifier,
            "tag": self.tag if self.tag is not None else "",
            "versions": [v.to_json() for v in self.versions],
        }

    @staticmethod
    def from_json(json: Dict[str, Any]):
        """Deserialize from JSON object."""
        assert all(
            n in json for n in ["identifier", "tag", "versions"]
        ), "Broken precondition."
        return Value(
            identifier=json["identifier"],
            tag=None if json["tag"] == "" else json["tag"],
            versions=[ResultVersion.from_json(v) for v in json["versions"]],
        )