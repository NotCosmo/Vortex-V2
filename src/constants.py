# General
from dataclasses import dataclass


# TODO: to be filled out with stuff from your guild cosmo
@dataclass
class GuildConstants:
    MAIN_GUILD_ID = 0
    TESTING_GUILDS = []
    QUOTE_CHANNEL_ID = 0
    LOGS_CHANNEL_ID = 0
    DEV_CHANNEL_ID = 0


@dataclass
class CustomConstants:
    # URLS
    DOG_URL = "https://api.thedogapi.com/v1/images/search"
    CAT_URL = "https://api.thecatapi.com/v1/images/search"
