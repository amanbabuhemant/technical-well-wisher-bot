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
import re 

if not TOKEN:
    print("Set TOKEN environment varibale")
    exit(1)

if not CHANNEL_ID:
    print("Please set CHANNEL_ID environment varibale")
    exit(1)


tracemalloc.start()





# Create instance of Client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Date Validation
async def sanitize_date(date, ctx):
    
    try:
        date = str(date).replace('"','').replace("'","")
        #for handling Leap and non-leap Year
        date_with_year = f"2004-{date}"
        sanitize_date = datetime.strptime(date_with_year, "%Y-%m-%d")
        return sanitize_date.strftime("%m-%d")

    except ValueError:
        
        await ctx.send("Invalid Date")
    

    

#Full_name Validation 
async def sanitize_full_name(full_name, ctx):
    full_name = str(full_name).replace('"','').replace("'","")
    pattern = "^[a-zA-Z]{3,}(?: [a-zA-Z]+){0,2}$"
    if re.match(pattern, full_name):
        return full_name
    else:
        await ctx.send("Please Write your Full_name Correctly.")



#CRUD OPERATION commands
session = Session(engine)

# add birthday
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.hybrid_command()
async def add(ctx, date=None, *, full_name: str):
        try:     
            await ctx.send("adding birthday")
                
            sanitize_name = await sanitize_full_name(full_name, ctx)
            sanitize_dt = await sanitize_date(date, ctx)
            if sanitize_name and sanitize_dt:
                print(sanitize_name)
                await ctx.send(f"date: {date} , full_name: {full_name}") 
                new_user = User(full_name=full_name, date_of_birth=date)
                session.add(new_user)
                session.commit()
        except ValueError:
            await ctx.send("Write Date and full Name Correctly")


@bot.hybrid_command()
async def fetch(ctx):
    await ctx.send(session.query(User).all())



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
   
