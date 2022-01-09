from discord import Bot
from discord import Cog as Extension


class RegistroSystem(Extension):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Extension.listener()
    async def on_raw_reaction_add(self, payload):
        # TODO: Implementar o registro de usuários
        pass


def setup(bot: Bot) -> None:
    bot.add_cog(RegistroSystem(bot))
