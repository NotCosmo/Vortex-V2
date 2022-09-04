import os

import nextcord
from nextcord.ext.commands import Bot

COGS = (f"cogs.{ext[:-3]}" for ext in os.listdir("./cogs") if ext.endswith(".py"))


class Vortex(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="-",
            case_insensitive=True,
            intents=nextcord.Intents.all(),
            strip_after_prefix=True,
        )

        self.colour = nextcord.Colour.from_rgb(0, 208, 255)
        self.icon = "https://cdn.discordapp.com/avatars/926513310642339891/36f01c4d80398bccdcf1ac094e6af7c4.png?size=1024"

    # Starts the bot
    async def start(self) -> None:
        
        for cog in COGS:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f"Could not load {cog} due to:\n{e}")
                
        await super().start(os.environ['token'])

    # Called when the bot is started
    async def on_ready(self) -> None:
        print("Bot is online.")
