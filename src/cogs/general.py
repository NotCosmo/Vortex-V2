from nextcord.ext.commands import Cog, command

from src.utility.bot import Vortex


class General(Cog, description="General commands of the bot."):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot

    @command(name="ping", help="Displays bot latency in ms.")
    async def ping(self, ctx):
        await ctx.send("Pong!")


def setup(bot: Vortex) -> None:
    print("General cog loaded.")
    bot.add_cog(General(bot))
