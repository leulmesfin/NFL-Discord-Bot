import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import nfl_stats
import aura

# STEP 0: Load our token from somwhere safe
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# We use the Client.event() decorator to register an event. Since the library
# is async, we do things in a "callback" style manner.
# A callback is a function that is called when something happens. 
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

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

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # This forwards the message to the command handler
    await bot.process_commands(message)

# Command handling with discord.ext.commands
@bot.command()
async def foo(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Gives you the live score of NFL games for the current week. 
# Also specifies the game date & broadcast channel
@bot.command()
async def nfl_scores(ctx):
    await ctx.send(nfl_stats.nfl_game_scores())

# Gives you the bye week teams
@bot.command()
async def bye_week(ctx):
    await ctx.send(nfl_stats.bye_week_teams())

# Gives you the passing yards leaders
@bot.command()
async def passing_yards(ctx):
    await ctx.send(nfl_stats.passing_yards())

# Gives you the rushing yards leaders
@bot.command()
async def rushing_yards(ctx):
    await ctx.send(nfl_stats.rushing_yards())

# Gives you the receiving yards leaders
@bot.command()
async def receiving_yards(ctx):
    await ctx.send(nfl_stats.receiving_yards())

# aura ranking
@bot.command()
async def aura_rank(ctx):
    await ctx.send(aura.aura_ranking())

@bot.command()
async def leul_him(ctx):
    await ctx.send("GOAT")

@bot.command()
async def ryan_him(ctx):
    await ctx.send("Ryan sold.")

# Run the bot
bot.run(TOKEN)