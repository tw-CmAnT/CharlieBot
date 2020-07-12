import discord
from discord.ext import commands
import config
from aiohttp import ClientSession
import random

class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_pet_embed(self, ctx: commands.Context, name: str):
        async with ClientSession() as cs:
            async with cs.get(f'https://tw2.pw/api/pet.php?pet={name}') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
    
        title = data['caption']
        url = data['url']
        pet_embed = discord.Embed(title=title, color=discord.Color(0x2AE150))
        pet_embed.set_image(url=url)
        await ctx.send(embed=pet_embed)

    async def create_embed_list(self, name: str):
        # create the embed lists here
        # get a list of all of pet's URLs
        #image_embed = discord.Embed(title=f'Woah {name} album!')
    
        #for url in url_list:
        #   image_embed.set_image(urll=url)
        #   embed_list.append('image_embed')

        #return embed_list

    
    @commands.command(brief='Posts a random dog pic')
    async def dog(self, ctx: commands.Context):
        async with ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
        
        url = data['message']
        dog_embed = discord.Embed(color=discord.Color.red())
        dog_embed.set_image(url=url)
        await ctx.send(embed=dog_embed)

    @commands.command(brief='Gives you a random dog fact', aliases=['dogfact'])
    async def fact(self, ctx: commands.Context):
        async with ClientSession() as cs:
            async with cs.get('https://dog-api.kinduff.com/api/facts') as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])

        await ctx.send(data['facts'][0])



    @commands.group(brief='The main commmand for posting pet pics!')
    async def pet(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('**Usage:**\n `,pet album <name>` or `,pet a <name>`\n `,pet random <name>` or `,pet r <name>`')

    @pet.command(brief='Posts a random image for a pet.', aliases=['random'])
    async def r(self, ctx: commands.Context, name: str = ''):
        if not name:
            await self.create_pet_embed(ctx, random.choice(config.pets_list))
        elif name not in config.pets_list:
            sorted_list = sorted(config.pets_list)
            description = "\n".join(sorted_list)
            embed = discord.Embed(title='Here is a List of Pets!', description=description)
            await ctx.send(embed=embed)
        else:
            await self.create_pet_embed(ctx, name)

    @pet.command(brief='Posts an album for a pet.', alises=['a'])
    async def album(self, ctx: commands.Context, name: str = ''):
        if (not name) or (name not in config.pets_list):
            sorted_list = sorted(config.pets_list)
            description = "\n".join(sorted_list)
            embed = discord.Embed(title='Here is a List of Pets!', description=description)
            await ctx.send(embed=embed)
        else:
            embeds = self.create_embed_list(name)
            await ctx.send('WIP command yuh yuh')

def setup(bot):
    bot.add_cog(Pets(bot))
