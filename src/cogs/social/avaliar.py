from discord import ApplicationContext, Embed, member
from discord import Bot, SlashCommandGroup
from discord import Cog as Extension
from discord import Option, Member
from discord.commands import slash_command

from src.accounts.server import CodifyCommunity
from src.accounts.users import DataBaseUser
from src.cooldown import Cooldown
import time


avaliarCoolDown = Cooldown(time.time() * 60 * 30)

class AvaliarCommands(Extension):
    def __init__(self, bot: Bot):
        self.bot = bot
    @slash_command(description="avaliar",  guild_ids=[743482187365613641])
    async def avaliar(self, it: ApplicationContext, down_or_up: Option(str, choices=["positivo", "negativo"]), membro: Option(Member, "membro para avaliar")):
        cooldown_key = (membro.id, it.author.id)

        if avaliarCoolDown.is_in_cooldown(cooldown_key):
            embed = Embed(title=f"Você está em cooldown!", color=0x738ADB)  
            return await it.send_response(embed=embed)

        if membro.id == it.author.id:
            embed = Embed(title=f"Voce não pode avaliar a você mesmo!", color=0x738ADB)  
            return await it.send_response(embed=embed)
        user = DataBaseUser(membro.id)

        if down_or_up == "positivo":
            await user.take_my_upvote()
        else: 
            await user.take_my_downvote()

        embed = Embed(title=f"Obrigado por avaliar {membro.name}", color=0x738ADB)
        avaliarCoolDown.update_or_add(cooldown_key)
        await it.send_response(embed=embed)

def setup(bot: Bot):
  bot.add_cog(AvaliarCommands(bot))