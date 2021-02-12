"""Handlers for responding to keywords in messages."""
from abc import ABC, abstractmethod


class MessageHandler(ABC):
    """Base class for responding to keywords in messages."""

    _keywords = []

    def should_respond(self, message):
        return any(keyword in message.content.lower() for keyword in self._keywords)

    @abstractmethod
    async def respond(self, message):
        """Check keywords and optionally respond to an incoming message."""


class Option6MessageHandler(MessageHandler):
    """Responds to mentions of Option 6."""

    _keywords = ["option 6", "option six"]

    async def respond(self, message):
        if self.should_respond(message):
            await message.channel.send(f"Are you talking behind my back, {message.author.name}?")


class DogMessageHandler(MessageHandler):
    """Responds like a dog."""

    _keywords = ["hello", "tea", "breakfast", "chicken", "custards", "walkies", "treat", "betty"]

    async def respond(self, message):
        if self.should_respond(message):
            await message.channel.send("Woof! Woof! Wag! Wag!")
