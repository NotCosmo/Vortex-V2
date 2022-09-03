import asyncio

from utility.bot import Vortex

bot = Vortex()
bot.remove_command("help")


async def main() -> None:
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
