import discord
from discord.ext import commands
from aiohttp import ClientSession
import random
import time

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def anilist_request(self, query: str, variables):
        url = 'https://graphql.anilist.co'
        async with ClientSession() as cs:
            async with cs.post(url, json={'query': query, 'variables': variables}) as r:
                data = await r.json()

        return r.status, data


    @commands.command(brief='Recommends a random high rated anime.', aliases=['rec', 'suggest', 'sug', 'rmd'])
    async def recommend(self, ctx: commands.Context):

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

        await ctx.send(embed=anime_embed)
    

def setup(bot):
    bot.add_cog(Anime(bot))