from datetime import datetime
from logging import info
from platform import python_version
from time import time

import humanize
import xmltodict
from nextcord import Color, Embed, Member, Spotify
from nextcord import __version__ as nc_ver
from nextcord.ext.commands import Cog, Context, command, guild_only
from psutil import Process, virtual_memory

from src.utility import util
from src.utility.bot import Vortex


class General(Cog, description="General commands of the bot."):
    def __init__(self, bot: Vortex) -> None:
        self.bot: Vortex = bot

    async def determine_party_host(self, member, activity):
        idd = int(activity.party_id.split(":")[1])
        if idd != member.id:
            usr = await self.bot.fetch_user(idd)
            party = str(usr)
        else:
            party = "Not in a party"
        return party

    @command(name="ping", help="Displays bot latency in ms.")
    async def ping(self, ctx: Context):
        start = time()
        message = await ctx.send(f"DWSP latency: {self.bot.latency * 1000:,.0f}ms")
        end = time()
        await message.edit(
            content=f"DWSP latency: {self.bot.latency * 1000:,.0f}ms || Response time: {(end - start) * 1000:,.0f}ms"
        )

    @command(
        name="userinfo", aliases=["ui"], brief="Shows a bunch of stuff about a user."
    )
    async def userinfo(self, ctx: Context, member: Member | None = None):
        member = member or ctx.author
        joined_days_ago = (
            datetime.today().replace(tzinfo=member.joined_at.tzinfo) - member.joined_at
        ).days
        created_days_ago = (
            datetime.today().replace(tzinfo=member.joined_at.tzinfo) - member.created_at
        ).days
        booster = (
            member.premium_since.strftime("%H:%M:%S, %d.%m.%Y")
            if member.premium_since
            else "No boosts."
        )
        nick = member.nick or "No custom nickname"

        colors = {
            "online": Color.green(),
            "idle": Color.yellow(),
            "dnd": Color.red(),
            "do_not_disturb": Color.red(),
            "offline": 0x696969,
            "invisible": 0x696969,
        }

        userinfo = Embed(
            title=f"{member} || {member.id}",
            description=f"Avatar URL: {member.avatar.with_size(4096).url}",
            color=colors.get(member.raw_status),
        )
        userinfo.set_thumbnail(url=member.avatar.with_size(4096).url)
        user = await self.bot.fetch_user(member.id)
        if user.banner:
            userinfo.set_image(user.banner.with_size(4096).url)
        userinfo.add_field(
            name="General",
            value=f"```Name: {member}\n"
            f"Status: {member.status} | Mobile: {member.is_on_mobile()}\n"
            f"Bot: {member.bot}\n"
            f"Joined Discord: {member.created_at.strftime('%H:%M:%S, %d.%m.%Y')} ({created_days_ago} days ago)\n```",
            inline=False,
        )
        userinfo.add_field(
            name="Server specific",
            value=f"```Nickname: {nick}\n"
            f"Boosting since: {booster}\n"
            f"Top Role: {member.top_role} (Color code: {member.top_role.color})\n"
            f"Joined server: {member.joined_at.strftime('%H:%M:%S, %d.%m.%Y')} ({joined_days_ago} days ago.)```",
            inline=False,
        )
        userinfo.add_field(
            name=f"Roles [{len(member.roles) - 1}]",
            value=" ".join([role.mention for role in member.roles[1:]]),
        )
        if member.voice:
            userinfo.add_field(
                name="Voice activity",
                value=f"```Current channel: {member.voice.channel.name}\n"
                f"Bitrate: {member.voice.channel.bitrate / 1000}kbit/s\n"
                f"User limit: {member.voice.channel.user_limit}\n"
                f"Streams: {member.voice.self_stream}\n"
                f"Video: {member.voice.self_video}"
                f"Muted: {member.voice.self_mute}\n"
                f"Deafened: {member.voice.self_deaf}\n"
                f"AFK: {member.voice.afk}```",
                inline=False,
            )
        for activity in member.activities:
            if isinstance(activity, Spotify):
                party = await self.determine_party_host(member, activity)
                artists = ", ".join(activity.artists)
                userinfo.add_field(
                    name="Spotify",
                    value=f"```Song: {activity.title} - {artists} | ({activity.album})\n"
                    f"Duration: {activity.duration}\n"
                    f"Party-Host: {party}\n"
                    f"Track ID: spotify:track:{activity.track_id}```",
                    inline=False,
                )

        userinfo.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.avatar.with_size(4096).url,
        )
        await ctx.send(embed=userinfo)

    @command(name="serverinfo", brief="Shows a bunch of stuff about the guild.")
    @guild_only()
    async def serverinfo(self, ctx: Context):
        days_ago = (
            datetime.today().replace(tzinfo=ctx.guild.created_at.tzinfo)
            - ctx.guild.created_at
        ).days
        mfa = "False" if ctx.guild.mfa_level == 0 else "True"
        description = (
            ctx.guild.description
            if ctx.guild.description is not None
            else "No description set."
        )
        serverinfo = Embed(
            title=f"{ctx.guild.name} || ID: {ctx.guild.id}",
            description=f"{description}",
            color=self.bot.main_color,
        )
        serverinfo.set_thumbnail(url=ctx.guild.icon.with_size(4096).url)
        serverinfo.add_field(
            name="Info",
            value=f"```Owner: {ctx.guild.owner}\n"
            f"Created at: {ctx.guild.created_at.strftime('%H:%M:%S, %d.%m.%Y')} ({days_ago} days ago)\n"
            f"AFK-Timeout: {int(ctx.guild.afk_timeout) / 60} minutes\n"
            f"System-Channel: {ctx.guild.system_channel}\n"
            f"Active invites: {len(await ctx.guild.invites())}\n"
            f"Active bans: {len(await ctx.guild.bans().flatten())}\n```",
            inline=False,
        )
        serverinfo.add_field(
            name="Stats",
            value=f"```Bot Count: {len(ctx.guild.bots)}\n"
            f"Member Count: {len(ctx.guild.humans)}\n"
            f"Total member count: {len(ctx.guild.members)}\n"
            f"Role count: {len(ctx.guild.roles)}\n"
            f"Channel count: {len(ctx.guild.channels)}\n"
            f"Bitrate limit: {ctx.guild.bitrate_limit / 1000}kbit/s\n"
            f"Emoji Limit: {ctx.guild.emoji_limit}```",
            inline=False,
        )
        serverinfo.add_field(
            name="Miscellaneous",
            value=f"```Large Server: {ctx.guild.large}\nVerification level: {ctx.guild.verification_level}\n2FA: {mfa}```",
            inline=False,
        )
        if ctx.guild.premium_tier > 0:
            serverinfo.add_field(
                name="Boosting stats",
                value=f"```Boost level: {ctx.guild.premium_tier}\nBoost Count: {ctx.guild.premium_subscription_count}```",
                inline=False,
            )
        await ctx.send(embed=serverinfo)

    @command(
        name="stats",
        aliases=["about", "info"],
        brief="Shows a bunch of stuff about the bot.",
    )
    async def stats(self, ctx: Context) -> None:
        stats_embed = Embed(
            title=f"Bot stats | Commands: {len(self.bot.commands)}",
            color=self.bot.main_color,
        )
        stats_embed.set_thumbnail(url=self.bot.user.display_avatar.with_size(4096).url)
        proc = Process()
        with proc.oneshot():
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            (
                "Bot version",
                f"v{self.bot.major_version}.{self.bot.minor_version}.{self.bot.patch_version}",
                True,
            ),
            ("Python version", python_version(), True),
            ("Nextcord version", nc_ver, True),
            ("Uptime", self.bot.get_uptime(), True),
            (
                "Memory usage",
                f"{mem_usage:,.3f} MiB / {mem_total:,.3f} MiB ({mem_of_total:.3f}%)",
                True,
            ),
            (
                "Popularity",
                f"{len(self.bot.users):,} users in {len(self.bot.guilds):,} servers",
                True,
            ),
            ("Developed by", f"<@{self.bot.owner_id}>", False),
        ]

        for name, value, inline in fields:
            stats_embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=stats_embed)

    @command(
        name="spotify", brief="Share what you are currently listening too on spotify."
    )
    async def spotify(self, ctx: Context, member: Member | None = None):
        member = member or ctx.author
        for activity in member.activities:
            if isinstance(activity, Spotify):
                party = await self.determine_party_host(member, activity)
                artists = ", ".join(artist for artist in activity.artists)
                spotify = Embed(
                    title=f"{activity.title} - {artists}",
                    description=f"from the album **{activity.album}**",
                    url=activity.track_url,
                    color=Color.green(),
                )
                spotify.set_thumbnail(url=activity.album_cover_url)
                spotify.add_field(
                    name="Duration",
                    value=str(activity.duration).split(".")[0],
                    inline=True,
                )
                spotify.add_field(name="Party", value=party, inline=True)
                spotify.set_footer(text=f"Track: {activity.track_url}")
                await ctx.send(embed=spotify)

    @command(name="apod", brief="Astronomy picture of the day")
    async def apod(self, ctx: Context):
        base_url = "https://api.nasa.gov/planetary/apod"
        params = {"api_key": self.bot.NASA_API_KEY}
        async with self.bot.aiohttp_session.get(base_url, params=params) as r:
            if r.status == 200:
                data = await r.json()
            else:
                return await ctx.send(f"Fetching {base_url} failed.")

        if data:
            apod_embed = Embed(
                title=data.get("title"),
                description=data.get("explanation"),
                color=self.bot.main_color,
            )

            author = f"Credits: {data.get('copyright', 'No credit found')}"
            apod_embed.set_footer(
                text=f"{author} | {util.format_date_from_string(data.get('date'))}"
            )

            if data.get("media_type") == "image":
                apod_embed.url = data.get("hdurl")
                apod_embed.set_image(url=data["hdurl"])

                await ctx.send(embed=apod_embed)
            elif data.get("media_type") == "video":
                # https://www.youtube.com/embed/ts0Ek3nLHew?rel=0 --> https://www.youtube.com/watch?v=ts0Ek3nLHew
                url: str = (
                    data.get("url").replace("?rel=0", "").replace("embed/", "watch?v=")
                )

                apod_embed.url = url

                await ctx.send(url)
                await ctx.send(embed=apod_embed)
            else:
                await ctx.send(
                    f"Unsupported media_type ({data.get('media_type')}), click link to see which data is present\n"
                    f"<{base_url}?api_key=DEMO_KEY>"
                )

    @command(name="weather", brief="Get weather info")
    async def weather(self, ctx: Context, *, city: str):
        US_EPA_INDEX = {
            1: "Good",
            2: "Moderate",
            3: "Unhealthy for sensitive group",
            4: "Unhealthy",
            5: "Very unhealthy",
            6: "Hazardous",
        }
        WIND_DIRECTIONS = {
            "N": "North",
            "NNE": "North-northeast",
            "NE": "Northeast",
            "ENE": "East-northeast",
            "E": "East",
            "ESE": "East-northeast",
            "SE": "Southeast",
            "SSE": "South-southeast",
            "S": "South",
            "SSW": "South-Southwest",
            "SW": "Southwest",
            "WSW": "West-southwest",
            "W": "West",
            "WNW": "West-northwest",
            "NW": "Northwest",
            "NNW": "North-northwest",
        }

        url = f"https://api.weatherapi.com/v1/current.json"
        params = {"key": self.bot.WEATHER_API_KEY, "q": city, "aqi": "yes"}
        async with self.bot.aiohttp_session.get(url, params=params) as r:
            if r.status == 200:
                data: dict = await r.json()
        try:
            location = data["location"]
            current = data["current"]
            condition = current["condition"]
            air_quality = current["air_quality"]
        except UnboundLocalError:
            return await ctx.send(
                "I don't rember this town, perhaps specify the country..?"
            )

        thumbnail_url = f"https:{condition['icon']}"

        weather_embed = Embed(
            title=f"Current weather in {location['name']}, {location['region']}, {location['country']} | {condition['text']}",
            description=f"Latitude: {location['lat']}, Longitude: {location['lon']}",
            color=self.bot.main_color,
        )

        weather_embed.set_thumbnail(url=thumbnail_url)
        weather_embed.set_footer(
            text=f"Last updated: {util.format_datetime_from_string(current['last_updated'])}"
        )

        weather_embed.add_field(
            name="Temperature",
            value=f"{current['temp_c']} C, Feels like: {current['feelslike_c']} C\n"
            f"{current['temp_f']} F, Feels like: {current['feelslike_f']} F",
        )
        weather_embed.add_field(
            name="Precipitation",
            value=f"{current['precip_mm']} mm | {current['precip_in']} inches",
        )
        weather_embed.add_field(
            name="Wind",
            value=f"{current['wind_kph']} km/h ({current['wind_mph']} mp/h)\n"
            f"Heading: {current['wind_dir']} | {WIND_DIRECTIONS[current['wind_dir']]}",
        )
        weather_embed.add_field(
            name="Pressure",
            value=f"{current['pressure_mb']} mbar | {current['pressure_in']} inHg",
        )

        extensive_air_quality = (
            f"CO: {round(air_quality['co'], 2)} µm/m^3\n"
            f"NO2: {round(air_quality['no2'], 2)} µm/m^3\n"
            f"O3: {round(air_quality['o3'], 2)} µm/m^3\n"
            f"SO2: {round(air_quality['so2'], 2)} µm/m^3\n"
            f"Dust (2.5µm): {round(air_quality['pm2_5'], 2)} µm/m^3\n"
            f"Dust (10 µm): {round(air_quality['pm10'], 2)} µm/m^3\n"
            f"EPA-Standard: {US_EPA_INDEX.get(air_quality['us-epa-index'])}"
        )

        weather_embed.add_field(
            name="Air quality",
            value=f"EPA-Standard: {US_EPA_INDEX.get(air_quality['us-epa-index'])}",
            inline=False,
        )

        await ctx.send(embed=weather_embed)

    @command(name="whatpulse", aliases=["wp"], brief="Get stats from a whatpulse user")
    async def whatpulse(self, ctx: Context, username: str):
        url = f"https://api.whatpulse.org/user.php"
        params = {"user": username}
        async with self.bot.aiohttp_session.get(url, params=params) as r:
            if r.status == 200:
                data: str = await r.text()

        data_dict = xmltodict.parse(data)
        data: dict = data_dict.get("WhatPulse")
        if not data:
            return await ctx.send("WhatPulse did not return any data.")

        if error := data.get("error"):
            return await ctx.send(f"WhatPulse returned an error: {error}")

        user_url = f"https://whatpulse.org/{data.get('AccountName')}"
        whatpulse_embed = Embed(
            title=f"Whatpulse stats {data.get('AccountName')}",
            url=user_url,
            color=self.bot.main_color,
        )

        userinfo = (
            f"Name: {data.get('AccountName')} (ID: {data.get('UserID')})\n"
            f"Country: {data.get('Country')}\n"
            f"Date joined: {util.format_date_from_string(data.get('DateJoined'))}\n"
        )
        whatpulse_embed.add_field(name="Userinfo", value=userinfo, inline=False)

        stats = (
            f"Pulses: {int(data.get('Pulses')):,}\n"
            f"Keys: {int(data.get('Keys')):,}\n"
            f"Clicks: {int(data.get('Clicks')):,}\n"
            f"Download: {data.get('Download')}\n"
            f"Upload: {data.get('Upload')}\n"
            f"Uptime: {data.get('UptimeLong')}\n"
            f"Avg. clicks per pulse: {int(data.get('AvClicksPerPulse')):,}\n"
            f"Avg. keys per pulse: {int(data.get('AvKeysPerPulse')):,}\n"
            f"Last pulse: {util.format_whatpulse_datetime(data.get('LastPulse'))}\n"
            f"Computers: {len(data.get('Computers'))}"
        )
        whatpulse_embed.add_field(name="Stats", value=stats, inline=False)

        ranks = data.get("Ranks")
        rank = (
            f"Keys: {humanize.ordinal(int(ranks.get('Keys')))}\n"
            f"Clicks: {humanize.ordinal(int(ranks.get('Clicks')))}\n"
            f"Download: {humanize.ordinal(int(ranks.get('Download')))}\n"
            f"Upload: {humanize.ordinal(int(ranks.get('Upload')))}\n"
            f"Uptime: {humanize.ordinal(int(ranks.get('Uptime')))}"
        )
        whatpulse_embed.add_field(name="Rank", value=rank, inline=False)

        await ctx.send(embed=whatpulse_embed)


def setup(bot: Vortex) -> None:
    bot.add_cog(General(bot))
