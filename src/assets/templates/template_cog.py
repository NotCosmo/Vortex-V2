from nextcord.ext.commands import Cog

from src.utility.bot import Vortex


class TemplateCog(Cog):
    def __init__(self, bot: Vortex):
        self.bot = bot


def setup(bot: Vortex):
    bot.add_cog(TemplateCog(bot))
