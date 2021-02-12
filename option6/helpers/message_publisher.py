"""Publisher that brokers message handler subscriptions."""
from typing import List

from option6.helpers.message_handler import MessageHandler


class MessagePublisher:
    """simple publisher to send messages to observers"""

    messageHandlers: List[MessageHandler] = []

    def subscribe(self, handler):
        self.messageHandlers.append(handler)

    async def publish(self, message):
        for handler in self.messageHandlers:
            await handler.handle(message)
