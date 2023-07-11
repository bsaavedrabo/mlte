"""
test/session/test_session.py

Unit tests for global session management.
"""

from mlte.session import (
    session_state,
    set_namespace,
    set_model,
    set_version,
    set_uri,
)


def test_session() -> None:
    namespace = "ns"
    model = "model"
    version = "v0.0.1"
    uri = "http://localhost:8080"

    set_namespace(namespace)
    set_model(model)
    set_version(version)
    set_uri(uri)

    s = session_state()

    assert s.context.namespace == namespace
    assert s.context.model == model
    assert s.context.version == version
    assert s.context.uri == uri
