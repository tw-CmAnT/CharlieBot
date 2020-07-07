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

async def create_pet_embed(ctx: commands.Context, name: str):
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
        async with cs.get('https://official-joke-api.appspot.com/jokes/random') as r:
            data = await r.json()
            if r.status != 200:
                await ctx.send(data['message'])
    
    await ctx.send(data['setup'])
    time.sleep(1)
    await ctx.send(data['punchline'])
            
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

# Start of Pet Commands #

@bot.group(brief='The main commmand for posting pet pics!')
async def pet(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        description = 'bella\n charlie\n coco\n cookie\n gem\n lucy\n mice\n norma\n pancake\n patches\n penny\n salem\n valkyrie\n whiskey'
        embed = discord.Embed(title='Here is a List of Pets!', description=description)
        await ctx.send(embed=embed)

@pet.command(brief='Posts a Bella pic <3')
async def bella(ctx: commands.Context):
    await create_pet_embed(ctx, 'bella')

@pet.command(brief='Posts a Charlie pic <3')
async def charlie(ctx: commands.Context):
    await create_pet_embed(ctx, 'charlie')

@pet.command(brief='Posts a Coco pic <3')
async def coco(ctx: commands.Context):
    await create_pet_embed(ctx, 'coco')

@pet.command(brief='Posts a Cookie pic <3 (the bird not the food)')
async def cookie(ctx: commands.Context):
    await create_pet_embed(ctx, 'cookie')

@pet.command(brief='Posts a Gem pic <3')
async def gem(ctx: commands.Context):
    await create_pet_embed(ctx, 'gem')

@pet.command(brief='Posts a Lucy pic <3')
async def lucy(ctx: commands.Context):
    await create_pet_embed(ctx, 'lucy')

@pet.command(brief='Posts a Mice pic <3')
async def mice(ctx: commands.Context):
    await create_pet_embed(ctx, 'mice')

@pet.command(brief='Posts a Norma pic <3')
async def norma(ctx: commands.Context):
    await create_pet_embed(ctx, 'norma')

@pet.command(brief='Posts a Pancake pic <3')
async def pancake(ctx: commands.Context):
    await create_pet_embed(ctx, 'pancake')

@pet.command(brief='Posts a Patches pic <3')
async def patches(ctx: commands.Context):
    await create_pet_embed(ctx, 'patches')

@pet.command(brief='Posts a Penny pic <3')
async def penny(ctx: commands.Context):
    await create_pet_embed(ctx, 'penny')

@pet.command(brief='Posts a Salem pic <3')
async def salem(ctx: commands.Context):
    await create_pet_embed(ctx, 'salem')

@pet.command(brief='Posts a Valkyrie pic <3')
async def valkyrie(ctx: commands.Context):
    await create_pet_embed(ctx, 'valkyrie')

@pet.command(brief='Posts a Whiskey pic <3')
async def whiskey(ctx: commands.Context):
    await create_pet_embed(ctx, 'whiskey')

# End of Pet Commands #

# Events

@bot.event
async def on_command_error(ctx: commands.Context, err: commands.CommandError):
    if isinstance(err, commands.CheckFailure):
        await ctx.send('You do not have permission to use this!')


bot.run(config.token)