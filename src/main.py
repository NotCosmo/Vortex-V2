from utility.bot import Vortex


def main() -> None:
    bot = Vortex()
    bot.remove_command("help")
    bot.run_bot()


if __name__ == "__main__":
    main()
