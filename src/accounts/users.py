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
    async def _reduce_user_coin(self, amount: int):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        
        await self.accounts.update_one({'userID': self.userID}, {'$inc': {'reaisCount': amount}})
        return True
    async def get_wallet(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['wallet']
    async def _add_coin_to_user_wallet(self, preco: int, coin: str, amount: int):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if coin not in user['wallet']:
            user['wallet'][coin] = 0
        for i in range(amount):
            user['wallet'][coin] += 1
        await self.accounts.update_one({'userID': self.userID}, {'$set': {'wallet': user['wallet']}})
        return True
    async def buy_coin(self, coin: str, coin_price: int, amount: int):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if user['reaisCount'] < amount * coin_price:
            return "Você não tem reais suficientes para comprar essa quantidade de moedas."
        else:
            await self._reduce_user_coin(amount * coin_price)
            await self._add_coin_to_user_wallet(coin_price, coin, amount)
            return True