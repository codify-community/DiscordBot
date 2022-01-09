from discord import ApplicationContext, Embed
from discord import Bot, SlashCommandGroup
from discord import Cog as Extension
from discord import Option, Member
from discord.commands import slash_command

from src.accounts.server import CodifyCommunity
from src.accounts.users import DataBaseUser


class LevelCommandos(Extension):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Mostra teu perfil atual", guild_ids=[743482187365613641])
    async def perfil(self, it: ApplicationContext, membro: Option(Member, "Membro para ver o level", required=False)):
        user = membro or it.author
        db_user = DataBaseUser(user.id)
        description = await db_user.get_description() or "Nenhuma descrição"
        server = CodifyCommunity()
        rank = None
        for r, member in enumerate(await server.rank_members()):
            if user.id == member.userID:
                rank = r + 1
                break

        saldo = await db_user.get_reais_count()
        nivel = await db_user.get_level()
        xp = await db_user.get_xp()
        next_level = await db_user.get_xp_required_for_next_level() + xp
        progress = int((xp / next_level) * 100)
        nick = user.nick or user.name if user != it.author else "mim"
        nboxes = int((xp / next_level) * 20)
        boxes = nboxes * ':blue_square:' + (20 - nboxes) * ':white_large_square:'
        embed = Embed(title=f"Sobre {nick}", color=user.color)
        embed.add_field(name='📝 Nome', value=f'{user.mention}', inline=True)
        embed.add_field(name='📝 Descrição', value=f'{description[0:24]}', inline=True)
        embed.add_field(name='<a:ff_fogo_padrao:809486155815845898> XP', value=f'` {xp} XP `', inline=True)
        embed.add_field(name='💸 saldo', value=f'` {saldo:.2f} FP `', inline=True)
        embed.add_field(name='⭐ Nível', value=f'`⠀⠀{nivel}⠀⠀`', inline=True)
        embed.add_field(name='🏆 Rank', value=f'`⠀{rank}°⠀`', inline=True)
        embed.add_field(name=f'Barra de Progresso ⠀⠀⠀⠀⠀   ⠀⠀ ⠀⠀⠀{xp}/{next_level} XP ({progress}%)',
                        value=boxes[0:1024], inline=False)
        embed.set_thumbnail(url=user.avatar.url)

        await it.respond(embed=embed)

    @slash_command(description="Nesse comando você define sua descrição",
                   guild_ids=[743482187365613641])
    async def descricao(self, it: ApplicationContext, descricao: Option(str, "Descrição para o seu perfil")):
        db_user = DataBaseUser(it.author.id)
        await db_user.set_description(descricao[0:1024])
        await it.respond("Descrição atualizada com sucesso!", ephemeral=True)

    top = SlashCommandGroup("top", "Mostra o top de usuários", guild_ids=[743482187365613641])

    @top.command(description="Mostra os niveis do servidor baseado na quantidade de dinheiro",
                 guild_ids=[743482187365613641])
    async def money(self, it: ApplicationContext, pagina: Option(int, "Pagina para ver os niveis", required=False)):
        page_list = lambda lst, x: [lst[i:i + x] for i in range(0, len(lst), x)]
        async with it.typing():
            pagina = pagina or 1
            server = CodifyCommunity()

            rank = await server.rank_members_money()
            pages = page_list(rank, 10)
            if pagina > len(pages):
                pagina = 1
            embed = Embed(title=f"Niveis do servidor (Dinheiro)", color=it.author.color)
            embed.description = ""
            embed.set_footer(text=f"Pagina {pagina}/{len(pages)}")
            guild = self.bot.get_guild(743482187365613641)
            for i, u in enumerate(pages[pagina - 1]):
                user = guild.get_member(u.userID)
                if user is not None and await u.get_reais_count() > 0:
                    embed.description += f"{i + 1}. [{user.name}#{user.discriminator}](https://discord.com/users/{user.id})" \
                                         f" - `R$ {await u.get_reais_count():.2f}`\n"
            await it.respond(embed=embed)

    @top.command(description="Mostra os niveis do servidor baseado no nível", guild_ids=[743482187365613641])
    async def level(self, it: ApplicationContext, pagina: Option(int, "Pagina para ver os niveis", required=False)):
        async with it.typing():
            page_list = lambda lst, x: [lst[i:i + x] for i in range(0, len(lst), x)]
            pagina = pagina or 1
            server = CodifyCommunity()

            rank = await server.rank_members()
            pages = page_list(rank, 10)
            if pagina > len(pages):
                pagina = 1
            embed = Embed(title=f"Niveis do servidor", color=it.author.color)
            embed.set_footer(text=f"Pagina {pagina}/{len(pages)}")
            guild = self.bot.get_guild(743482187365613641)
            embed.description = ""
            for i, u in enumerate(pages[pagina - 1]):
                user = guild.get_member(u.userID)
                if user is not None and await u.get_level() > 0:
                    embed.description += f"{i + 1}. [{user.name}#{user.discriminator}](https://discord.com/users/{user.id})" \
                                         f" - `Nível: {await u.get_level()}`\n"
            await it.respond(embed=embed)


def setup(bot: Bot):
    bot.add_cog(LevelCommandos(bot))
