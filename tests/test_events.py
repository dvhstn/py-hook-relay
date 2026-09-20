from uuid import UUID

import pytest
from pydantic import ValidationError

from hookrelay.events import Event


def test_event_generates_id_and_timestamp() -> None:
    event = Event(event_type="release.published", payload={"action": "published"})

    assert isinstance(event.id, UUID)
    assert event.created_at is not None


def test_event_requires_event_type() -> None:
    with pytest.raises(ValidationError):
        Event(payload={"action": "published"})
