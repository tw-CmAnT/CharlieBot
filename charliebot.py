import discord
from discord.ext import commands
import praw
import config
from aiohttp import ClientSession
import random
import time
from cogs import pets
import traceback


class CharlieBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial_extensions = (
            'cogs.pets',
            'cogs.anime',
            'cogs.misc'
        )

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except:
                print(f'Failed to load {extension}')
                print(traceback.format_exc())
    



bot = CharlieBot(command_prefix=',')
bot.run(config.token)
