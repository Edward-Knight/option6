"""Handlers for responding to keywords in messages."""
from random import choice
from typing import Optional, Sequence, Set


class MessageHandler:
    """Base class for responding to keywords in messages."""

    keywords: Set[str] = set()
    responses: Optional[Sequence[str]] = None

    def should_respond(self, message) -> bool:
        """Check if {self.keywords} are in {message}."""
        return any(keyword in message.content.casefold() for keyword in self.keywords)

    async def respond(self, message) -> None:
        """Optionally respond to an incoming message."""
        if self.should_respond(message):
            await message.reply(choice(self.responses))


class Option6MessageHandler(MessageHandler):
    """Responds to mentions of Option 6."""

    keywords = ["option 6", "option six"]

    async def respond(self, message):
        if self.should_respond(message):
            await message.reply(f"Are you talking behind my back, {message.author.display_name}?")


class DogMessageHandler(MessageHandler):
    """Responds like a dog."""

    keywords = ["hello", "tea", "breakfast", "chicken", "custards", "walkies", "treat", "betty"]
    responses = ["Arf!", "Bark!", "Woof!", "_excitedly wags tail_"]
