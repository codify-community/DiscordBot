import time

from discord import ApplicationContext, Embed
from discord import Bot
from discord import Cog as Extension
from discord import Option, Member
from discord.commands import slash_command

from src.accounts.users import DataBaseUser
from src.cooldown import Cooldown
from src.utils.embeds import simple_embed, Kind

avaliarCoolDown = Cooldown(round(time.time() * 60 * 30))


class AvaliarCommands(Extension):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Nesse comando você pode avaliar um membro", guild_ids=[743482187365613641])
    async def avaliar(self, it: ApplicationContext, opcao: Option(str, choices=["positivo", "negativo"]),
                      membro: Option(Member, "membro para avaliar")):
        cooldown_key = (membro.id, it.author.id)

        if avaliarCoolDown.is_in_cooldown(cooldown_key):
            return await it.respond(embed=simple_embed("Erro", "Você está em cooldown", Kind.Error), ephemeral=True)

        if membro.id == it.author.id:
            return await it.respond(embed=simple_embed("Erro", "Você não pode avaliar você mesmo", Kind.Error), ephemeral=True)
        user = DataBaseUser(membro.id)

        if opcao == "positivo":
            await user.take_my_upvote()
        else:
            await user.take_my_downvote()

        avaliarCoolDown.update_or_add(cooldown_key)
        embed = simple_embed("Você avaliou com sucesso!", f"Você avaliou {membro.mention}! yay!")
        await it.send_response(embed=embed, ephemeral=True)


def setup(bot: Bot):
    bot.add_cog(AvaliarCommands(bot))
