import discord
from discord.ext import commands
from aiohttp import ClientSession
import random
from bot.paginators import EmbedPaginator
from bot.reddit import Reddit 

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def anilist_request(self, query: str, variables):
        url = 'https://graphql.anilist.co'
        async with ClientSession() as cs:
            async with cs.post(url, json={'query': query, 'variables': variables}) as r:
                data = await r.json()

        return r.status, data

    def create_anime_embed(self, anime):
        title = anime['title']['romaji']
        score = anime['meanScore']
        description = anime['description']
        genres = ", ".join(anime['genres'])
        image = anime['coverImage']['large']
        url = anime['siteUrl']

        embed_title = f'{title} ({score}/100)'
        embed_description = f'**Genres**: {genres}\n \n {description}'

        anime_embed = discord.Embed(title=embed_title, description=embed_description, url=url)
        anime_embed.set_image(url=image)

        return anime_embed

    @commands.group()
    async def anime(self, ctx: commands.Context):
        '''The main commmand for anime!'''
        if ctx.invoked_subcommand is None:
            await ctx.send('**Usage:** \n `,anime recommend/rec/rmd`\n `,anime search/s <name>`\n `anime meme`')

    @anime.command(aliases=['rec', 'rmd'])
    async def recommend(self, ctx: commands.Context):
        '''Recommends a random high rated anime.'''
        
        # First Request:
        query = '''
        query ($page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    currentPage
                    lastPage
                    perPage
                }
                media (type: ANIME, averageScore_greater: 75) {
                    id
                }
            }
        }
        '''

        variables = {
            'page': 1,
            'perPage': 5
        }       

        status_code, data = await self.anilist_request(query, variables)

        if status_code != 200:
            await ctx.send(data['errors'][0]['message'])
        
        pages_amount = data['data']['Page']['pageInfo']['lastPage']

        # Second Request:

        query = '''
        query ($page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    perPage
                }
                media (type: ANIME, averageScore_greater: 75) {
                    title {
                        romaji
                    }
                    description(asHtml: false)
                    meanScore
                    genres
                    coverImage {
                        large
                        medium
                    }
                    siteUrl
                }
            }
        }
        '''

        variables = {
            'page': random.randint(1, pages_amount),
            'perPage': 5
        }

        status_code, data = await self.anilist_request(query, variables)

        if status_code != 200:
            await ctx.send(data['errors'][0]['message'])
        
        page = data['data']['Page']['media']
        anime = page[random.randint(0, len(page) - 1)]

        anime_embed = self.create_anime_embed(anime)

        await ctx.send(embed=anime_embed)
    
    @anime.command(aliases=['s'])
    async def search(self, ctx: commands.Context, name: str = ''):
        '''Searches for an anime by name'''
        query = '''
        query ($page: Int, $perPage: Int, $search: String) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    perPage
                }
                media (type: ANIME, search: $search) {
                    title {
                        romaji
                    }
                    meanScore
                    description(asHtml: false)
                    genres
                    coverImage {
                        large
                        medium
                    }
                    siteUrl
                }
            }
        }
        '''

        variables = {
            'page': 1,
            'perPage': 5,
            'search': name
        }

        status_code, data = await self.anilist_request(query, variables)

        if status_code != 200:
            await ctx.send(data['errors'][0]['message'])
        
        page = data['data']['Page']['media']
        total = data['data']['Page']['pageInfo']['total']
        pages_amount = data['data']['Page']['pageInfo']['lastPage']
        anime_amount = int(total / pages_amount)


        #loop through media and get the anime list and paginate them
        embed_list = []
        for i in range(anime_amount):
            anime = page[i]
            anime_embed = self.create_anime_embed(anime)
            embed_list.append(anime_embed)
        
        if anime_amount == 0:
            await ctx.send(f'{name} Not Found!')
        elif anime_amount == 1:
            await ctx.send(embed=embed_list[0])
        else:
            paginator = EmbedPaginator(embeds=embed_list)
            await paginator.run(ctx) 
    
    @anime.command()
    async def meme(self, ctx: commands.Context):
        '''Get a random anime meme'''
        reddit = Reddit()
        submission = reddit.get_random_submission('Animemes')
        embed = discord.Embed(title=submission.title)
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def jojo(self, ctx: commands.Context):
        '''Get a random jojo post'''
        subs_list = ['ShitPostCrusaders', 'StardustCrusaders', 'wholesomejojo']
        subreddit_name = random.choice(subs_list)

        reddit = Reddit()
        submission = reddit.get_random_submission(subreddit_name)
        embed = discord.Embed(title=submission.title)
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)
         

def setup(bot):
    bot.add_cog(Anime(bot))