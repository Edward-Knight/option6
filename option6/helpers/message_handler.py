"""Handlers for responding to keywords in messages."""
import random
from typing import Optional, Sequence, Set


class MessageHandler:
    """Base class for responding to keywords in messages."""

    keywords: Set[str] = set()
    responses: Optional[Sequence[str]] = None
    chance: float = 1.0

    def should_respond(self, message) -> bool:
        """Will return {True} if {self.keywords} are in {message},
        and if we hit the specified random chance.
        """
        return (
            any(keyword in message.content.casefold() for keyword in self.keywords)
            and self.chance > random.random()
        )

    async def respond(self, message) -> None:
        """Optionally respond to an incoming message."""
        if self.should_respond(message):
            await message.reply(random.choice(self.responses))


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
