import datetime
import logging
import os
import time
from typing import Optional

import aiohttp
import nextcord
from dotenv import load_dotenv
from nextcord.ext.commands import Bot

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)


class Vortex(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=os.getenv("BOT_PREFIX"),
            case_insensitive=True,
            intents=nextcord.Intents.all(),
            strip_after_prefix=True,
            owner_id=int(os.getenv("BOT_OWNER_ID")),
        )
        # Internal Stuff
        self.aiohttp_session: Optional[aiohttp.ClientSession] = None
        self.token: Optional[str] = os.getenv("BOT_TOKEN")
        self.icon = "https://cdn.discordapp.com/avatars/926513310642339891/36f01c4d80398bccdcf1ac094e6af7c4.png?size=4096"
        self.start_time = time.time()
        self.owner_id = int(os.getenv("BOT_OWNER_ID"))

        # API Keys
        self.NASA_API_KEY = os.getenv("NASA_API_KEY")
        self.WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

        # Versioning
        self.major_version, self.minor_version, self.patch_version = os.getenv("BOT_VERSION").split(".")

        # Somewhat globals
        self.main_color: int = 0x00D0FF

    def get_uptime(self) -> datetime.timedelta:
        difference = int(time.time() - self.start_time)
        uptime = datetime.timedelta(seconds=difference)
        return uptime

    def load_dir(self, directory: str) -> None:
        files = [
            file[:-3] for file in os.listdir(directory) if not file.startswith("__")
        ]
        for file in files:
            ext = f"{directory}.{file}"
            self.load_extension(ext)
            logging.info(f"{ext} loaded successfully")

    def load_cogs(self) -> None:
        self.load_dir("cogs")
        self.load_extension("jishaku")
        logging.info("loading extensions finished")

    def load_tasks(self) -> None:
        self.load_dir("tasks")
        logging.info("loading tasks finished")

    async def register_aiohttp_session(self) -> None:
        self.aiohttp_session = aiohttp.ClientSession()

    def run_bot(self) -> None:
        logging.info("starting up...")
        self.loop.create_task(self.register_aiohttp_session())
        self.load_cogs()
        self.load_tasks()
        super().run(self.token)

    # Events
    async def on_ready(self) -> None:
        logging.info(f"ready as {self.user} / {self.user.id}")

    async def catdog(self, url):
        async with self.aiohttp_session.get(url) as r:
            if r.status == 200:
                response = await r.json()
        return response[0].get("url")
