"""Handlers for responding to keywords in messages."""
import random
import string
from abc import ABC, abstractmethod
from typing import Sequence, Set, Type


class MessageHandler(ABC):
    """Base class for detecting keywords in messages."""

    keywords: Set
    """Keywords to look for in a message.

    Must be lower case.
    """

    def should_respond(self, message) -> bool:
        """Will return {True} if {self.keywords} are in {message},
        and if we hit the specified random chance.
        """
        return any(keyword in message.content.casefold() for keyword in self.keywords)

    @abstractmethod
    async def handle(self, message) -> None:
        """Handle an incoming message."""


class RandomMessageHandler(MessageHandler, ABC):
    """Adds a random chance to not handle a message."""

    chance: float
    """Random chance that handle will get called, in the range 0 to 1."""

    def should_respond(self, message) -> bool:
        """Will return {True} if {self.keywords} are in {message},
        and if we hit the specified random chance.
        """
        return self.chance > random.random() and super().should_respond(message)


class MessageResponder(MessageHandler):
    """Base class for responding to messages containing keywords."""

    responses: Sequence[str]
    """A list of responses to randomly choose from."""

    async def handle(self, message):
        """Optionally respond to an incoming message."""
        if self.should_respond(message):
            await message.reply(random.choice(self.responses))


class MessageReactor(MessageHandler):
    """Base class for emoji reacting to messages containing keywords."""

    emojis: Sequence[str]
    """A list of emoji to randomly choose from."""

    async def handle(self, message) -> None:
        """Optionally reacts to an incoming message."""
        if self.should_respond(message):
            await message.add_reaction(random.choice(self.emojis))


class Option6MessageResponder(RandomMessageHandler, MessageResponder):
    """Responds to mentions of Option 6."""

    keywords = {"option 6", "option six"}
    chance = 0.1

    async def handle(self, message):
        if self.should_respond(message):
            await message.reply(f"Are you talking behind my back, {message.author.display_name}?")


class DogMessageResponder(MessageResponder):
    """Responds like a dog."""

    keywords = {"hello", "tea", "breakfast", "chicken", "custards", "walkies", "treat", "betty"}
    responses = ["Arf!", "Bark!", "Woof!", "_excitedly wags tail_"]


class GoodBotReactor(MessageReactor):
    """Receives praise for being a good bot."""

    keywords = {"good bot", "who's a good boy"}
    emojis = [
        "❤",
        "️💛",
        "💓",
        "💕",
        "💖",
        "💗",
        "💘",
        "💙",
        "💚",
        "💜",
        "💝",
        "💞",
        "🖤",
        "😍",
        "😘",
        "🤍",
        "🤎",
        "🥰",
    ]


class ShittyReactor(MessageReactor, RandomMessageHandler):
    """Randomly awards people with poop."""

    keywords = string.ascii_lowercase
    chance = 0.001
    emojis = ["💩"]


HANDLERS: Set[Type[MessageHandler]] = {
    Option6MessageResponder,
    DogMessageResponder,
    GoodBotReactor,
    ShittyReactor,
}
