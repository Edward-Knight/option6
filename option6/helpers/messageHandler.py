class messageHandler:
    _keywords = []

    def shouldRespond(self, message):
        return any(keyword in message.content.lower() for keyword in self._keywords)

class option6MessageHandler(messageHandler):
    _keywords = ["option 6", "option six"]
    async def respond(self, message):
        if(self.shouldRespond(message)):
            await message.channel.send(f"Are you talking behind my back, {message.author.name}?")


class dogMessageHandler(messageHandler):
    _keywords = ["hello", "tea", "breakfast", "chicken", "custards", "walkies", "treat", "betty"]

    async def respond(self, message):
        if(self.shouldRespond(message)):
            await message.channel.send("Woof! Woof! Wag! Wag!")