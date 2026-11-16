from sqlalchemy.orm import Session
from datetime import datetime
import asyncio
import tracemalloc
import discord
from discord import Message
from discord.ext import commands
from env import *
from database.models.user import User
from database.models import engine
 

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

#CRUD OPERATION commands
session = Session(engine)

# add birthday
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.hybrid_command()
async def add(ctx, date, full_name):
    await ctx.send("adding birthday")
    new_user = User(full_name=full_name, date_of_birth=date)
    session.add(new_user)
    session.commit()

    



# on ready start event of warnings and error

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



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


# run bot and client

bot.run(TOKEN)

client.run(TOKEN)
   
