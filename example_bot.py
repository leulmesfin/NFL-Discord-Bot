from typing import Final
import discord
import os
from dotenv import load_dotenv

# create an instance of a Client. This client is our connection to Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# STEP 0: Load our token from somwhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# We use the Client.event() decorator to register an event. Since the library
# is async, we do things in a "callback" style manner.
# A callback is a function that is called when something happens. 

# The on_ready() event is called when 
# the bot has finished logging in and setting things up.

# The on_message() event is called when the bot has received a message.
# Since the on_message() event triggers for every message received, we have
# to make sure that we ignore messages from ourselves. We do this by checking if
# the Message.author is the same as the Client.user.

# Then, we check if the Message.content starts with '$hello'. If it does, we send
# a message in the channel it was used in with 'Hello!'. This is a basic way of 
# handing commands, which can be later automated with discord.ext commands.

# Finally, we run the bot with our login token.

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)