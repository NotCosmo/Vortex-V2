import nextcord
from nextcord import Embed, slash_command, Interaction
from nextcord.ext.commands import command, Cog, Context
from utility.bot import Vortex

class HelpDropdown(nextcord.ui.Select):

    def __init__(self, bot: Vortex):
        options = [
            nextcord.SelectOption(
                label="ℹ️ General", description="Shows general commands."
            ),
            nextcord.SelectOption(
                label=":hammer_pick: Moderation", description="Shows moderation commands."
            )
        ]

        self.bot: Vortex = bot
        super().__init__(
            placeholder="Choose what category you want",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):

        if self.values[0] == "ℹ️ General":

            cog_selected = self.bot.get_cog("General")
            embed = Embed(title=self.values[0], description=cog_selected.description, colour=self.bot.colour)
            embed.set_thumbnail(url=self.bot.icon)
            for cmd in cog_selected.get_commands():
                if not cmd.hidden:
                    embed.add_field(name=f"{self.bot.command_prefix}{cmd.name}", value=cmd.help, inline=True)
            await interaction.response.send_message(embed=embed)

class DropdownView(nextcord.ui.View):
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
    print("Help loaded.")
    bot.add_cog(Help(bot))