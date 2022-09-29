from logging import info

from nextcord import Embed, Interaction, SelectOption, ui
from nextcord.ext.commands import Cog, Context, command

from src.utility.bot import Vortex


class HelpDropdown(ui.Select):
    def __init__(self, bot: Vortex):
        options = [
            SelectOption(label="ℹ️ General", description="Shows general commands."),
            SelectOption(
                label=":hammer_pick: Moderation",
                description="Shows moderation commands.",
            ),
        ]

        self.bot: Vortex = bot
        super().__init__(
            placeholder="Choose what category you want",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: Interaction):

        if self.values[0] == "ℹ️ General":

            cog_selected = self.bot.get_cog("General")
            embed = Embed(
                title=self.values[0],
                description=cog_selected.description,
                colour=self.bot.main_color,
            )
            embed.set_thumbnail(url=self.bot.icon)

            cmds_text = ""
            count = 0
            for cmd in cog_selected.get_commands():
                if not cmd.hidden:
                    count += 1
                    cmds_text += f"{cmd.name}, "

            embed.add_field(name=f"Commands [{count}]", value=cmds_text, inline=True)
            await interaction.response.send_message(embed=embed)


class DropdownView(ui.View):
    def __init__(self, bot: Vortex):
        self.bot: Vortex = bot
        super().__init__()

        self.add_item(HelpDropdown(bot))


class Help(Cog):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot

    """
    @slash_command(guild_ids=[581139467381768192], description="Shows descriptions of every command.")
    async def help(self, interaction: Interaction):
        await interaction.response.send_message("Help")
    """

    @command(name="help")
    async def help(self, ctx: Context):

        view = DropdownView(self.bot)
        await ctx.send("Choose", view=view)


def setup(bot: Vortex) -> None:
    bot.add_cog(Help(bot))
    info(f"{Help.__class__.__name__} cog loaded.")
