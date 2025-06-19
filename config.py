import os

class BotConfig:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.cogs = [
        ]

