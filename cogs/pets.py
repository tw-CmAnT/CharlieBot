import discord
from discord.ext import commands
import config
from aiohttp import ClientSession
import random
from bot.paginators import EmbedPaginator
from bot.reddit import Reddit 

class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_pet_embed(self, ctx: commands.Context, name: str):
        async with ClientSession() as cs:
            async with cs.get(f'https://tw2.pw/api/pet/?name={name}') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
    
        title = f'{name} is here!!'
        url = random.choice(data['pictures'])
        pet_embed = discord.Embed(title=title, color=discord.Color(0x2AE150))
        pet_embed.set_image(url=url)
        await ctx.send(embed=pet_embed)

    async def create_embed_album(self, ctx: commands.Context, name: str):
        async with ClientSession() as cs:
            async with cs.get(f'https://tw2.pw/api/pet/?name={name}') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])

        pictures_list = data['pictures']
        embed_list = []
        for url in pictures_list:
            image_embed = discord.Embed(title=f'Woah {name} album!')
            image_embed.set_image(url=url)
            embed_list.append(image_embed)

        paginator = EmbedPaginator(embeds=embed_list)
        await paginator.run(ctx)

    
    @commands.command()
    async def aww(self, ctx: commands.Context):
        '''Get a random cute image'''
        reddit = Reddit()
        submission = reddit.get_random_submission('aww')

        embed = discord.Embed(title=submission.title)
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
                

    @commands.command()
    async def dog(self, ctx: commands.Context):
        '''Posts a random dog pic'''
        async with ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
        
        url = data['message']
        dog_embed = discord.Embed(color=discord.Color.red())
        dog_embed.set_image(url=url)
        await ctx.send(embed=dog_embed)

    @commands.command(aliases=['dogfact'])
    async def fact(self, ctx: commands.Context):
        '''Gives you a random dog fact'''
        async with ClientSession() as cs:
            async with cs.get('https://dog-api.kinduff.com/api/facts') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])

        await ctx.send(data['facts'][0])

    # Pet Commands:

    @commands.group()
    async def pet(self, ctx: commands.Context):
        '''The main commmand for posting pet pics!'''
        if ctx.invoked_subcommand is None:
            await ctx.send('**Usage:**\n `,pet album <name>` or `,pet a <name>`\n `,pet random <name>` or `,pet r <name>`')

    @pet.command(aliases=['random'])
    async def r(self, ctx: commands.Context, name: str = ''):
        '''Posts a random image for a pet.'''
        if not name:
            await self.create_pet_embed(ctx, random.choice(config.pets_list))
        elif name not in config.pets_list:
            sorted_list = sorted(config.pets_list)
            description = "\n".join(sorted_list)
            embed = discord.Embed(title='Here is a List of Pets!', description=description)
            await ctx.send(embed=embed)
        else:
            await self.create_pet_embed(ctx, name)

    @pet.command(aliases=['a'])
    async def album(self, ctx: commands.Context, name: str = ''):
        '''Posts an album for a pet.'''
        if (not name) or (name not in config.pets_list):
            sorted_list = sorted(config.pets_list)
            description = "\n".join(sorted_list)
            embed = discord.Embed(title='Here is a List of Pets!', description=description)
            await ctx.send(embed=embed)
        else:
            await self.create_embed_album(ctx, name)

def setup(bot):
    bot.add_cog(Pets(bot))
