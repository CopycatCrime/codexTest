from dotenv import load_dotenv
import os

load_dotenv()

class BotConfig:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.cogs = [
        ]
        

