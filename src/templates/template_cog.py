import logging

import nextcord
from nextcord.ext.commands import Cog, Context, command

from src.utility.bot import Vortex


class TemplateCog(Cog, description="General commands of the bot."):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot


def setup(bot: Vortex) -> None:
    bot.add_cog(TemplateCog(bot))
