from discord.commands import ApplicationContext, Option
from discord.commands import slash_command, SlashCommandGroup
from discord import Bot
helper = SlashCommandGroup(
    "helper", description="Helper Commands", guild_ids=[743482187365613641],)


@helper.command()
async def dar(
        context: ApplicationContext,
        tipo: Option(str,  "qual a linguagem que você quer ajudar",  choices=["Rust", "JavaScript", "PHP"])):
    await context.respond('Testando felas das maes.\n')


@helper.command()
async def ser(
        context: ApplicationContext,
        tecnologia: Option(str,  "Tecnologia",  choices=["Geral",
            "Go",
            "Rust",
            "Lua",
            "C e C++",
            ".NET",
            "Python",
            "Databases",
            "Java",
            "JavaScript"])):
    await context.respond('Testando felas das maes.\n')


def setup(bot: Bot):
    bot.add_application_command(helper)
