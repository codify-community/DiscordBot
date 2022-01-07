from src.database import database
from pymongo.database import Database


class DataBaseUser:
    def __init__(self, userID):
        self.discordDatabase: Database = database()['discord']
        self.accounts = self.discordDatabase.get_collection('Accounts')
        self.userID = userID
    async def _injector(self):
        if await self.accounts.find_one({'userID': self.userID}) is None:
            await self.accounts.insert_one({"userID": self.userID, "reaisCount": 0, "karma": {"upvotes": 0, "downvotes": 0}, "wallet": {}, "warnings": [], 'xp': 0, "level": 0, "description": None})
    async def get_reais_count(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['reaisCount']