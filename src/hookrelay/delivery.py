import json

import httpx

from hookrelay.events import Event
from hookrelay.signing import sign_payload


def deliver(event: Event, url: str, secret: str) -> httpx.Response:
    body = json.dumps(event.payload).encode()
    headers = {
        "Content-Type": "application/json",
        "X-HookRelay-Event": event.event_type,
        "X-HookRelay-Delivery": str(event.id),
        "X-Hub-Signature-256": sign_payload(body, secret),
    }
    return httpx.post(url, content=body, headers=headers)
