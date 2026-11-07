from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import asyncio
import tracemalloc
import discord
from discord.ext import commands


from env import *


if not TOKEN:
    print("Set TOKEN environment varibale")
    exit(1)

if not CHANNEL_ID:
    print("Please set CHANNEL_ID environment varibale")
    exit(1)


tracemalloc.start()


# engine = create_engine('sqlite://database/bot.db')

# Create instance of Client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



# bot commands 

bot = commands.Bot(command_prefix='$', intents = intents)

@bot.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')


# on ready start event of warnings and error

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

# main on connect event 
@client.event 
async def on_connect():

    await asyncio.sleep(5)
    channel = client.get_channel(CHANNEL_ID)
    await wish(channel)

# recursive function of checking date for wishes
async def wish(channel): 
    today = datetime.now()    
    today = str(today.strftime("%m-%d"))
    if today == "11-05":
        print("Artizote Birthday")
        await channel.send("@ghostor._. kya nakli id banaty ho drift")


# bot.add_command(test)

client.run(TOKEN)
   
