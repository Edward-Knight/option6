"""Tests for option6.helpers.message_handler."""
import pytest

from option6.helpers.message_handler import MessageHandler, PhraseMessageHandler


class _TestMessage:
    def __init__(self, message: str):
        self.content = message


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

    fake_message = _TestMessage(message)
    handler = TestMessageHandler()

    assert handler.should_respond(fake_message) == should_respond


@pytest.mark.parametrize(
    "message, should_respond",
    [
        ("test", True),
        ("TEST", True),
        ("Match on test.", True),
        ("intestine", True),
    ],
)
def test_phrase_recognition(message: str, should_respond: bool):
    class TestPhraseHandler(PhraseMessageHandler):
        keywords = {"test"}

        async def handle(self, _message) -> None:
            pass

    fake_message = _TestMessage(message)
    handler = TestPhraseHandler()

    assert handler.should_respond(fake_message) == should_respond
