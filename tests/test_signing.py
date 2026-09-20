from hookrelay.signing import sign_payload


def test_sign_payload_matches_known_answer() -> None:
    signature = sign_payload(b"Hello, World!", secret="It's a Secret to Everybody")

    assert signature == "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"


def test_sign_payload_differs_by_secret() -> None:
    payload = b'{"action": "published"}'

    assert sign_payload(payload, secret="secret-a") != sign_payload(payload, secret="secret-b")
