from app.logging_config import scrub_event
from app.pii import scrub_text, scrub_value


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_value_redacts_nested_log_content_without_changing_metrics() -> None:
    value = {
        "payload": {
            "contacts": ["student@vinuni.edu.vn", {"phone": "090 123 4567"}],
            "card": "4111-1111-1111-1111",
        },
        "latency_ms": 123.4,
    }

    cleaned = scrub_value(value)

    assert cleaned["payload"]["contacts"][0] == "[REDACTED_EMAIL]"
    assert cleaned["payload"]["contacts"][1]["phone"] == "[REDACTED_PHONE_VN]"
    assert cleaned["payload"]["card"] == "[REDACTED_CREDIT_CARD]"
    assert cleaned["latency_ms"] == 123.4


def test_scrub_event_redacts_exception_and_nested_payload() -> None:
    event = {
        "event": "request_failed for student@vinuni.edu.vn",
        "exception": "Contact 0901234567",
        "payload": {"details": {"cccd": "001234567890"}},
    }

    cleaned = scrub_event(None, "error", event)

    serialized = str(cleaned)
    assert "student@vinuni.edu.vn" not in serialized
    assert "0901234567" not in serialized
    assert "001234567890" not in serialized
