import config
import discord
from discord.ext import commands
from aiohttp import ClientSession
import random
import time

bot = commands.Bot(command_prefix=',')

# Helpers

def has_role_or_above(role_id: int):
    async def predicate(ctx):
        role = ctx.guild.get_role(role_id)
        return ctx.author.top_role >= role
    return commands.check(predicate)

def is_cmant(discord_id: int):
    async def predicate(ctx):
        return ctx.author.id == discord_id
    return commands.check(predicate)


# Bot Commands

@bot.command(brief='Says hi to you')
@has_role_or_above(370426390324969482)
async def hello(ctx: commands.Context):
    await ctx.send(f'Hi {ctx.author.mention} <3')

@bot.command(brief='Repeats after you, like an echo!')
@has_role_or_above(370426390324969482)
async def echo(ctx: commands.Context, *, text: str):
    await ctx.send(text)

@bot.command(brief='Mutes a person', aliases=['m'])
@has_role_or_above(370426390324969482)
async def mute(ctx: commands.Context, *, target: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Test')
    await target.add_roles(role)
    await ctx.send(f'Muted {target.display_name}')

@bot.command(brief='Posts a Charlie pic <3')
async def charlie(ctx: commands.Context):
    charlie_embed = discord.Embed(title='Charlie Is Here!', description='Woof Woof', color=discord.Color.blurple())
    url = random.choice(config.charlie_list)
    charlie_embed.set_image(url=url)
    await ctx.send(embed=charlie_embed)

@bot.command(brief='Posts a Coco pic <3')
async def coco(ctx: commands.Context):
    coco_embed = discord.Embed(title='Coco Is Here!', description='Follow Coco @ https://www.instagram.com/xrangii/', color=discord.Color.gold())
    url = random.choice(config.coco_list)
    coco_embed.set_image(url=url)
    await ctx.send(embed=coco_embed)

@bot.command(brief='Posts a Patches pic <3')
async def patches(ctx: commands.Context):
    patches_embed = discord.Embed(title='I am an autistic cat!', description='Woof Woof', color=discord.Color.purple())
    url = random.choice(config.patches_list)
    patches_embed.set_image(url=url)
    await ctx.send(embed=patches_embed)

@bot.command(brief='Posts a Cookie pic <3 (the bird not the food)')
async def cookie(ctx: commands.Context):
    cookie_embed = discord.Embed(title='Cookie Is Here!', color=discord.Color(0xFF00EC))
    url = random.choice(config.cookie_list)
    cookie_embed.set_image(url=url)
    await ctx.send(embed=cookie_embed)

@bot.command(brief='Posts a Gem pic <3')
async def gem(ctx: commands.Context):
    gem_embed = discord.Embed(title='Gem Is Here!', color=discord.Color(0xFF00EC))
    url = random.choice(config.gem_list)
    gem_embed.set_image(url=url)
    await ctx.send(embed=gem_embed)

@bot.command(brief='Posts a Bella pic <3')
async def bella(ctx: commands.Context):
    async with ClientSession() as cs:
        async with cs.get('https://tw2.pw/api/bella.php') as r:
            data = await r.json()
            if r.status != 200:
                await ctx.send(data['message'])
    
    title = data['caption']
    url = data['url']
    bella_embed = discord.Embed(title=title, color=discord.Color(0xDA71DA))
    bella_embed.set_image(url=url)
    await ctx.send(embed=bella_embed)


@bot.command(brief='Displays your profile', aliases=['pf'])
async def profile(ctx: commands.Context):
    embed = discord.Embed(title=ctx.author.display_name, description='Charlie Cult Member')
    embed.set_image(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(brief='Find out what Charlie thinks about you!')
async def tbh(ctx: commands.Context):
    await ctx.send(':thinking:')
    await ctx.send(f'tbh... Charlie thinks that you are a cutie! {ctx.author.mention}')

@bot.command(brief='Tells you a joke')
async def joke(ctx: commands.Context):
    async with ClientSession() as cs:
        async with cs.get('https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist&type=single') as r:
            data = await r.json()
            if r.status != 200:
                await ctx.send(data['message'])
    
    await ctx.send(data['joke'])
            
@bot.command(brief='Posts a random dog pic')
async def dog(ctx: commands.Context):
    async with ClientSession() as cs:
        async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
            data = await r.json()
            if r.status != 200:
                await ctx.send(data['message'])
    
    url = data['message']
    dog_embed = discord.Embed(color=discord.Color.red())
    dog_embed.set_image(url=url)
    await ctx.send(embed=dog_embed)

@bot.command(brief='Gives you a random dog fact', aliases=['dogfact'])
async def fact(ctx: commands.Context):
    async with ClientSession() as cs:
        async with cs.get('https://dog-api.kinduff.com/api/facts') as r:
            data = await r.json()
            if r.status != 200:
                await ctx.send(data['message'])

    await ctx.send(data['facts'][0])

# Events

@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError):
    if isinstance(err, commands.CheckFailure):
        await ctx.send('You do not have permission to use this!')


bot.run(config.token)