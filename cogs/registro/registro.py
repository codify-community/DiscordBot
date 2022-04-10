import discord
from discord.ext import commands
import asyncio
from utils.mongoconnect import mongoConnect

cluster = mongoConnect()
db = cluster['codify']
conta = db['conta']

def get_role_id(category, emoji):
    general_roles = {
        #default config
        "1️⃣":743504369059889178,
        "2️⃣":743504370913509406,
        "3️⃣":743504376496259164,
        "4️⃣":743504676292657203,
        "5️⃣":743504686392279121,
        "🚹":743525068868550657,
        "🚺":743525096676655185,
        "🚼":821454370120925225,
        "🟩":743529159833288794,
        "🟢":743529159690682528,
        "🟦":743527187533004870,
        "🔵":743527185712808146,
        "🟪":743529159552139286,
        "🟣":743529159296286772,
        "🌷":743528964479254538,
        "🌸":743528962474377227,
        "🟥":743527183821308046,
        "🔴":743527181975552051,
        "🟧":743527179257774241,
        "🟠":743527162732216392,
        "🟨":743527160903368808,
        "🟡":743527159406002238,
        "⬜":743528960373293066,
        "⬛":743528957369909339,
        #languages
        "<:xx_c_:745084475402354718>":745234055804616765,
        "<:xx_C_:745084615160758352>":745234075131969546,
        "<:xx_csharp:745084850838569161>":745234102952787969,
        "<:xx_css:745084407265624244>":745234022149390367,
        "<:xx_html:745084335299887144>":745233977304023110,
        "<:xx_java:745084182354460742>":745233859116793906,
        "<:xx_JavaScript:745084094840438895>":745233933330939944,
        "<:xx_php:819281651631652896>":745234155129929738,
        "<:xx_python:745084957587931277>":745234190915731560,
        "<:xx_rust:819278093759807498>":844221994010411038,
        "<:xx_lua:759787810382675968>":808106726116425758,
        "<:xx_golang:819280057179832320>":844222602021175356,
        "<:xx_elixir:904837194852761600>":904837424574758952,
        "<:xx_ruby:904833654432337950>":904834425567711253,
        #IDEs/text editors
        "<:xy_vscode:819282673670291547>":745293963828658176,
        "<:xy_jetbrains:745085628571582464>":745294152429994064,
        "<:xy_sublimetext:745086136371642418>":745294098520342631,
        "<:xy_eclipse:745086369029685301>":745294034116804628,
        "<:xy_netbeans:746884552395325490>":746884082771689522,
        "<:xy_vim:815271719824130058>":844232644966613012,
        "<:xx_emacs:912057023514951771>":844232638222303303,
        #area
        "⌨️":761022873762005023,
        "🚫":842729167887401000,
        "<:xa_designer:778104411711995934>":761023038279122985,
        "<:bb_terminal:770642267463614504>":761023097666797608,
        "<:xa_gamedev:778102624792477707>":778101737562701825,
        "<:xa_frontend:778107468458098688>":778101499309850624,
        "<:xa_backend:778106636593266699>":778101501460611072,
        "<:xa_fullstack:778103884341575720>":778100207400648704,
        "<:xa_bancodedados:778103884433588235>":771802609509466182,
        "<:xa_servidor:778102616810192897>":778101688983748649,
        "<:xa_mobile:778103884853936159>":778101496822497322,
        "<:xa_desktop:778103885147406356>":778101642112401408,
        #verification and notifications
        "✅":745666021024858194,
        "🔔":778068609951989850
    }
    helper_roles = {
        "<:xx_c_:745084475402354718>":904487025070202880,
        "<:xx_csharp:745084850838569161>":904487465983836210,
        "<:xx_html:745084335299887144>":904487582161829908,
        "<:xx_JavaScript:745084094840438895>":904485429896679464,
        "<:xx_php:819281651631652896>":904486369349496922,
        "<:xx_java:745084182354460742>":904487962128027748,
        "<:xx_python:745084957587931277>":904486056739631174,
        "<:xx_rust:819278093759807498>":904485830792462336,
        "<:xx_lua:759787810382675968>":904488063168831558,
        "<:xx_golang:819280057179832320>":904487915940376636,
        "<:xx_elixir:904837194852761600>":904829041259970601,
        "<:xa_servidor:778102616810192897>":904829006501793892,
        "<:xa_fullstack:778103884341575720>":904834155030937650,
        "<:xa_bancodedados:778103884433588235>":904513289998970890,
        "<:bb_terminal:770642267463614504>":904484232645197845
    }
    objects = {'general':general_roles, 'helper':helper_roles}

    return(objects[category][emoji])

class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = str(payload.emoji)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = message.guild
        user = await guild.fetch_member(payload.user_id)
        channels = {743490687353487460:'general', 904532938341896233:'helper'}
        try:
            role_id = get_role_id(channels[channel.id], emoji)
            role = guild.get_role(int(role_id))
            await user.add_roles(role)
        except:
            pass


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = str(payload.emoji)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = message.guild
        user = await guild.fetch_member(payload.user_id)
        channels = {743490687353487460:'general', 904532938341896233:'helper'}
        try:
            role_id = get_role_id(channels[channel.id], emoji)
            role = guild.get_role(int(role_id))
            await user.remove_roles(role)
        except:
            pass

def setup(bot):
    bot.add_cog(Registro(bot))
