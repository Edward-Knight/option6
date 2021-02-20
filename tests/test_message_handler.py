"""Tests for option6.helpers.message_handler."""
import pytest

from option6.helpers.message_handler import MessageHandler


@pytest.mark.parametrize(
    "message, should_respond",
    [
        ("test", True),
        ("TEST", True),
        ("Match on test.", True),
        ("intestine", False),
    ],
)
def test_word_recognition(message: str, should_respond: bool):
    class TestMessageHandler(MessageHandler):
        keywords = {"test"}

        async def handle(self, _message) -> None:
            pass

    class TestMessage:
        content = message

    fake_message = TestMessage()
    handler = TestMessageHandler()

    assert handler.should_respond(fake_message) == should_respond
