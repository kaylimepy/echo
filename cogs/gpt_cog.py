import discord
from discord import app_commands
from discord.ext import commands
from lib.gpt import chat

class GptCog(commands.Cog):
    '''GPT-3 commands'''
    @app_commands.command(name='echo')
    @app_commands.describe(message='What do you want to say to Echo?')
    async def echo(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(chat(message))


async def setup(bot: commands.Bot) -> None:
  '''Load the GPT-3 cog'''
  await bot.add_cog(GptCog())
