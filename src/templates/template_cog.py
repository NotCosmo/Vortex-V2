import logging

from nextcord import Embed, Member
from nextcord.ext.commands import Cog, Context, command

from src.utility.bot import Vortex


class TemplateCog(Cog, description="General commands of the bot."):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot


def setup(bot: Vortex) -> None:
    bot.add_cog(TemplateCog(bot))
    logging.info(f"{TemplateCog.__class__.__name__} cog loaded.")