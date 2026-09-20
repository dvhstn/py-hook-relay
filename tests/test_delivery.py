import json

import httpx
import respx

from hookrelay.delivery import deliver
from hookrelay.events import Event
from hookrelay.signing import sign_payload


@respx.mock
def test_deliver_sends_signed_post() -> None:
    route = respx.post("https://example.com/webhook").mock(return_value=httpx.Response(200))
    event = Event(event_type="release.published", payload={"action": "published"})

    response = deliver(event, "https://example.com/webhook", secret="test-secret")

    assert response.status_code == 200
    sent_request = route.calls.last.request
    expected_body = json.dumps(event.payload).encode()
    assert sent_request.content == expected_body
    assert sent_request.headers["X-HookRelay-Event"] == "release.published"
    assert sent_request.headers["X-HookRelay-Delivery"] == str(event.id)
    assert sent_request.headers["X-Hub-Signature-256"] == sign_payload(
        expected_body, secret="test-secret"
    )
