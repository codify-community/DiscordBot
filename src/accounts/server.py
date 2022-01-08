from pymongo.database import Database

from src.accounts.users import DataBaseUser
from src.database import database


class CodifyCommunity:
    def __init__(self):
        self.discordDatabase: Database = database()['discord']
        self.accounts = self.discordDatabase.get_collection('Accounts')

    async def rank_members_money(self) -> list[DataBaseUser]:
        rankings = self.accounts.find().sort('reaisCount', -1)
        result = []
        async for member in rankings:
            result.append(DataBaseUser(member['userID']))
        return result

    async def rank_members(self) -> list[DataBaseUser]:
        rankings = self.accounts.find().sort('level', -1)
        result = []
        async for member in rankings:
            result.append(DataBaseUser(member['userID']))
        return result
