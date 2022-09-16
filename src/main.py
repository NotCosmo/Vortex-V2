from utility.bot import Vortex

bot = Vortex()
bot.remove_command("help")


def main() -> None:
    bot.run_bot()


if __name__ == "__main__":
    main()
