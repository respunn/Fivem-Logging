import asyncio
# Importing modules from separate file
from important_files.imports import *

#You need to create ".env" file for secure your token then import it.
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Import the cogs
from cogs.log_commands import log_commands
# from cogs.race_commands import race_commands

async def setup():
    # Assigning bot.
    bot = commands.Bot(command_prefix='!', intents= discord.Intents.all())
    bot.remove_command('help')

    # Add the cogs to the bot (await the add_cog() method calls)
    await bot.add_cog(log_commands(bot))
    # await bot.add_cog(race_commands(bot))

    # To get a reaction and enter details when the bot is ready.
    @bot.event
    async def on_ready():
        # Setting status.
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
        # Printing bot's details.
        print('Connected to bot: {}'.format(bot.user.name))
        print('Bot ID: {}'.format(bot.user.id))
        try:
            # Trying to sync commands.
            sycned = await bot.tree.sync()
            print(f'Sycned {len(sycned)} global commands.')
        except Exception as e:
            print(e)
    
    await bot.start(TOKEN)

asyncio.run(setup())