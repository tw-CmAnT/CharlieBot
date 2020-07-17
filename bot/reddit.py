import discord
from discord.ext import commands
import praw
import config

class Reddit:
    
    def __init__(self):
        reddit = praw.Reddit(client_id = config.client_id,
                             client_secret = config.client_secret,
                             user_agent = config.user_agent)
        
        self.reddit = reddit
    
    def get_random_submission(self, subreddit_name: str, avoid_spoilers: bool = True, is_image: bool = True):
        reddit = self.reddit
        subreddit = reddit.subreddit(subreddit_name)

        submission = next(subreddit.random_rising())

        while (is_image and (submission.is_self or submission.domain != 'i.redd.it')) or (avoid_spoilers and submission.spoiler):
            submission = next(subreddit.random_rising())
        
        return submission