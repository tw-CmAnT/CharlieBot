import discord
from discord.ext import commands
from aiohttp import ClientSession
import random
import time

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='Displays your profile', aliases=['pf'])
    async def profile(self, ctx: commands.Context):
        embed = discord.Embed(title=ctx.author.display_name, description='Charlie Cult Member')
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(brief='Find out what Charlie thinks about you!')
    async def tbh(self, ctx: commands.Context):
        await ctx.send(':thinking:')
        await ctx.send(f'tbh... Charlie thinks that you are a cutie! {ctx.author.mention}')

    @commands.command(brief='Tells you a joke')
    async def joke(self, ctx: commands.Context):
        async with ClientSession() as cs:
            async with cs.get('https://official-joke-api.appspot.com/jokes/random') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
        
        await ctx.send(data['setup'])
        time.sleep(1)
        await ctx.send(data['punchline'])


def setup(bot):
    bot.add_cog(Misc(bot))
