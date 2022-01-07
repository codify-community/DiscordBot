import os
class Config:
    """
    The abstration based on bot dotenv
    """
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.statusWebhook = os.getenv("DISCORD_WEBHOOK")
        self.databaseURL = os.getenv("DATABASE_URL")
        self.logsChannel = os.getenv("DISCORD_LOG_CHANNEL") or 929055399049592862
        self.isOnDevEnv = True if os.getenv("PRODUCTION") == "false" else False
        self.version = os.getenv("CODIFY_BOT_VERSION") or "0.0.0"