from discord import Interaction
from discord import ui
from discord.enums import ButtonStyle
from discord.ui import View, Button


class Confirm(View):
    def __init__(self):
        super().__init__()
        self.value = False

    @ui.button(label='Sim', style=ButtonStyle.primary)
    async def confirm_true(self, _button: Button, _it: Interaction):
        self.value = True
        self.stop()

    @ui.button(label='Não', style=ButtonStyle.danger)
    async def confirm_false(self, _button: Button, _it: Interaction):
        self.value = False
        self.stop()
