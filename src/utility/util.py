import os
import textwrap
from datetime import date, datetime, time
from typing import Optional

from nextcord.ext import commands
from nextcord.ext.commands import Group


class NotImplementedYet(NotImplementedError):
    def __init__(self):
        super().__init__("This command has not been implemented yet.")


def list_options(command: Optional[Group]) -> str:
    if command:
        params = ", ".join(
            f"`!!{cmd.qualified_name}`" for cmd in commands.Group.walk_commands(command)
        )
    else:
        params = "No subcommands available."
    return params


def format_time(obj: time) -> str:
    """:return: string like "15:45:12" """
    return obj.strftime("%H:%M:%S")


def format_date(obj: date) -> str:
    """:return: string like "01.06.2022" """
    return obj.strftime("%d.%m.%Y")


def format_date_from_string(x: str) -> str:
    """:return: parse date from "2022-06-01" string and return "01.06.2022" """
    obj = datetime.strptime(x, "%Y-%m-%d")
    return format_date(obj)


def format_datetime_from_string(x: str) -> str:
    """:return: parse date from "2022-06-01 15:45" string and return "01.06.2022" """
    obj = datetime.strptime(x, "%Y-%m-%d %H:%M")
    return format_date_time(obj)


def format_to_db_date(obj: date) -> str:
    """:return:string like "2022-06-01" """
    return obj.strftime("%Y-%m-%d")


def format_to_db_datetime(obj: datetime) -> str:
    """:return: string like "2022-06-01 15:45:12" """
    return obj.strftime("%Y-%m-%d %H:%M:%S")


def format_date_time(obj: datetime) -> str:
    """:return: string like "15:45:12, 01.06.2022" """
    return obj.strftime("%H:%M:%S, %d.%m.%Y")


def format_whatpulse_datetime(x: str) -> str:
    """
    :return: parse date from "2022-06-01 15:45:12" string and return "15:45:12, 01.06.2022"
    """
    obj = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    return format_date_time(obj)


def pascal_case(string):
    return "".join(x.capitalize() for x in string.split("_"))


def surround_each_letter(message: str, surrounding_char: str):
    return "".join(f"{surrounding_char}{x}{surrounding_char}" for x in message)


def spoiler_each_letter(message: str):
    return surround_each_letter(message, "||")


def italic_each_letter(message: str):
    return surround_each_letter(message, "*")


def bold_each_letter(message: str):
    return surround_each_letter(message, "**")


def italic_bold_each_letter(message: str):
    return surround_each_letter(message, "***")


def surround_message(message: str, surrounding_char: str):
    return f"{surrounding_char}{message}{surrounding_char}"


def spoiler_message(message: str):
    return surround_message(message, "||")


def italic_message(message: str):
    return surround_message(message, "*")


def bold_message(message: str):
    return surround_message(message, "**")


def italic_bold_message(message: str):
    return surround_message(message, "***")


def create_cog_function(cog_name: str):
    class_name = pascal_case(cog_name)
    path = os.getcwd()
    with open(f"{path}/cogs/{cog_name}.py", "w") as f:
        to_write = textwrap.dedent(
            f"""
        from nextcord import Embed, Message, Member
        from nextcord.ext.commands import Cog, command, group, Context

        from src.utility.bot import Vortex


        class {class_name}(Cog):
            def __init__(self, bot: Vortex):
                self.bot: Vortex = bot


        def setup(bot: Vortex):
            bot.add_cog({class_name}(bot))
            """
        )
        f.write(to_write)
