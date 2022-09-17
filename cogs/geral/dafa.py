from discord import Member
from discord.ext.commands import Cog, Context, command


class DontAskForAsk(Cog):
    def __init__(self) -> None:
        pass

    @command(aliases=["dafa", "npap"])
    async def naopergunteparaperguntar(self, cx: Context, membro: Member):
        await cx.send(
            f"""{membro.mention}, você não precisa perguntar para perguntar.

Em vez disso, envie sua dúvida de forma clara, detalhada e objetiva.
Assim você se ajuda a ser ajudado.

Exemplos:

❌Errado
Alguém consegue me tirar uma dúvida?

✅ Certo
Envie sua duvida no fórum <#1019636543486439585> (ou em algum forúm na catego\
ria da sua duvida) com as devidas tags.

> Preciso listar todos os itens de um array, mas não estou sabendo como.
> O que já fiz: https://www.online-python.com/example
> Alguém saberia como?

Para enviar código, envie lá.
Para enviar imagens/arquivos, envie lá.
"""
        )


def setup(bot):
    bot.add_cog(DontAskForAsk())
