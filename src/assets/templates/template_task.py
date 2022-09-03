import logging
from datetime import time

from nextcord.ext import commands, tasks

from src.utility.bot import Vortex


class TemplateCog(commands.Cog):
    def __init__(self, bot: Vortex):
        self.bot = bot
        self.template_task.start()

    def cog_unload(self) -> None:
        self.template_task.cancel()

    @tasks.loop(time=time(hour=10, minute=00))
    async def template_task(self):
        pass

    @template_task.before_loop
    async def before_task(self) -> None:
        await self.bot.wait_until_ready()
        logging.log(msg=f"{self.__class__.__name__} started", level=logging.INFO)


def setup(bot: Vortex):
    bot.add_cog(TemplateCog(bot))
