import logging
import random

from pymongo.database import Database

from src.database import database

_get_xp_by_level = lambda level: round((50 * (level ** 2)) + (50 * level))


class DataBaseUser:
    def __init__(self, userID):
        self.discordDatabase: Database = database()['discord']
        self.accounts = self.discordDatabase.get_collection('Accounts')
        self.userID = userID

    async def _injector(self):
        if await self.accounts.find_one({'userID': self.userID}) is None:
            await self.accounts.insert_one(
                {"userID": self.userID, "reaisCount": 0, "karma": {"upvotes": 0, "downvotes": 0}, "wallet": {},
                 "warnings": [], 'xp': 0, "level": 0, "description": None})

    async def get_reais_count(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['reaisCount']

    async def _inc_user_coins(self, amount: float):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})

        await self.accounts.update_one({'userID': self.userID}, {'$inc': {'reaisCount': amount}})
        return True

    async def get_wallet(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['wallet']

    async def _add_coin_to_user_wallet(self, preco: int, coin: str, amount: float):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if coin not in user['wallet']:
            user['wallet'][coin] = 0
        user['wallet'][coin] += amount
        await self.accounts.update_one({'userID': self.userID}, {'$set': {'wallet': user['wallet']}})
        return True

    async def _remove_coins_to_user_wallet(self, preco, coin, amount):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if coin not in user['wallet']:
            return False
        if user['wallet'][coin] < amount:
            return False
        else:
            user['wallet'][coin] -= amount
            await self.accounts.update_one({'userID': self.userID}, {'$set': {'wallet': user['wallet']}})
            return True

    async def sell_coins(self, coin: str, coin_price: int, amount: float):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if coin not in user['wallet'] or user['wallet'][coin] < amount:
            return f"Você não tem {coin} suficientes para vender essa quantidade."
        else:
            await self._remove_coins_to_user_wallet(coin_price, coin, amount)
            await self._inc_user_coins(amount * coin_price)
            return True

    async def get_price_after_discount(self, coin_price: int):
        await self._injector()
        lvl = await self.get_level()
        max_lvl = 500 if lvl > 500 else lvl  # 500 is the max level to get shit
        # é velho tem q ter IF se não vai dar merda kek
        if max_lvl == 0:
            return coin_price
        return round(coin_price - ((0.05 * max_lvl / 100) * coin_price))

    async def _inc_karma(self, amount: int):  # vamo fzr uma gambiarra fodaseeeeeeeeee
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if amount >= 1:
            user['karma']['upvotes'] += amount
        else:
            user['karma']['downvotes'] -= amount

        await self.accounts.update_one({'userID': self.userID}, {'$set': {'karma': user['karma']}})

    async def take_my_upvote(self):
        await self._inc_karma(1)

    async def take_my_downvote(self):
        await self._inc_karma(-1)

    async def get_upvotes(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['karma']['upvotes']

    async def get_downvotes(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['karma']['downvotes']

    async def get_karma(self):
        return await self.get_upvotes() - await self.get_downvotes()

    async def buy_coin(self, coin: str, coin_price: int, amount: float):
        await self._injector()
        price_after_discount = await self.get_price_after_discount(coin_price)

        if await self.get_reais_count() < amount * price_after_discount:
            return "Você não tem reais suficientes para comprar essa quantidade de moedas."
        else:
            await self._inc_user_coins(-(amount * price_after_discount))
            await self._add_coin_to_user_wallet(price_after_discount, coin, amount)
            return True

    async def transfer_reais(self, userID: int, amount: float):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        if user['reaisCount'] < amount:
            return "Você não tem reais suficientes para transferir essa quantidade de moedas."
        else:
            await self._inc_user_coins(-amount)
            user = DataBaseUser(userID)
            await user._inc_user_coins(amount)
            return True

    async def daily(self) -> int:
        rand = random.randint(10, 100)
        await self._inc_user_coins(rand)
        return rand

    async def increase_level_by(self, amount: int):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        user['level'] += amount
        await self.accounts.update_one({'userID': self.userID}, {'$set': {'level': user['level']}})

    async def get_level(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['level']

    async def get_xp(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['xp']

    async def increase_xp_by(self, amount: int):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        xp = user['xp']
        xp += amount
        required = await self.get_xp_required_for_next_level()
        logging.getLogger(__name__).info("XP: " + str(xp) + " | Required: " + str(required) + "\n\t| User: "
                                         + str(self.userID))
        if amount < 64:
            amount = 64
        if required <= 0:  # level up
            await self.increase_level_by(1)
            await self.accounts.update_one({'userID': self.userID}, {'$inc': {'xp': amount}})
            return True

        await self.accounts.update_one({'userID': self.userID}, {'$inc': {'xp': amount}})

        return False

    async def get_xp_required_for_next_level(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return _get_xp_by_level(await self.get_level() + 1) - user['xp']

    async def set_description(self, description: str):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        user['description'] = description
        await self.accounts.update_one({'userID': self.userID}, {'$set': {'description': user['description']}})

    async def get_description(self):
        await self._injector()
        user = await self.accounts.find_one({'userID': self.userID})
        return user['description']
