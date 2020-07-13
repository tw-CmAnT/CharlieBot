import discord
from discord.ext import commands
from typing import List
import asyncio

class EmbedPaginator:

    def __init__(self, embeds: List[discord.Embed], left_emoji: str = None, right_emoji: str = None):
        self._embeds = embeds
        self._pointer = 0
        
        if right_emoji is None:
            self._right_emoji = '➡️'
        if left_emoji is None:
            self._left_emoji = '⬅️'

        self._running = False

    @property
    def current_embed(self):
        try:
            return self._embeds[self._pointer]
        except IndexError:
            return self._embeds[0]

    async def run(self, ctx: commands.Context):

        self._running = True
        msg = await ctx.send(embed=self.current_embed)
        await msg.add_reaction(self._left_emoji)
        await msg.add_reaction(self._right_emoji)

        def msg_react(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author and str(reaction) in (self._right_emoji, self._left_emoji)

        while self._running:

            # Wait for a reaction to the embed message, only reactions from the user and with left/right reactions will count
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', check=msg_react, timeout=15.0)
            except asyncio.TimeoutError:
                break

            await reaction.remove(ctx.author)

            # Now adjust the pointer for the embed that should be displayed
            if str(reaction) == self._right_emoji:
                self._pointer += 1
                if self._pointer == len(self._embeds):
                    self._pointer = 0
            elif str(reaction) == self._left_emoji:
                if self._pointer == 0:
                    self._pointer = len(self._embeds) - 1
                else:
                    self._pointer -= 1
            
            # Set the embed on the message
            await msg.edit(embed=self.current_embed)
    
    async def stop(self):
        self._running = False
        
