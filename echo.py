import discord
from discord.ext import commands
import lib.config as config

MY_GUILD = discord.Object(id=config.read('discord', 'guild_id'))

class Echo(commands.Bot):
    '''Echo Bot'''
    async def setup_hook(self):
        await self.load_extension('cogs.gpt_cog')

        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

bot = Echo(command_prefix='$', intents=discord.Intents.default())
bot.run(config.read('discord', 'bot_token'))
