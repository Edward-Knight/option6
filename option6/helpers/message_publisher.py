"""Publisher that brokers message handler subscriptions."""


class MessagePublisher:
    """simple publisher to send messages to observers"""

    _messageHandlers = []

    def subscribe(self, handler):
        self._messageHandlers.append(handler)

    async def publish(self, message):
        for handler in self._messageHandlers:
            await handler.respond(message)
