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


#Sanitization
date_pattern = "^[0-9]{2}-[0-9]{2}"
full_name_pattern = "^[a-zA-Z]{3,}(?: [a-zA-Z]+){0,2}$"


#Date Validation
async def sanitize_date(date, ctx,dt_pattern=date_pattern):
    
    try:
        date = str(date).replace('"','').replace("'","")
        #for handling Leap and non-leap Year

        if re.match(dt_pattern, date):
            date_with_year = f"2004-{date}"
            sanitize_date = datetime.strptime(date_with_year, "%Y-%m-%d")
            return sanitize_date.strftime("%m-%d")
        else:
            await ctx.send("Write Date in Correct Format MM-DD")

    except ValueError:
        
        await ctx.send("Write Date in Correct Format MM-DD")
    

    

#Full_name Validation 
async def sanitize_full_name(full_name, ctx,name_pattern = full_name_pattern):
    s_full_name =  str(full_name).replace("'","").replace('"','')
    if re.match(name_pattern, s_full_name):
        return s_full_name
    else:
        await ctx.send("Please Write your Full_name Correctly.")


#id Validation

async def sanitize_id(id,ctx):
    try:
        s_id = int(id)
        if s_id:
            return s_id
    except:
        await ctx.send("Enter correct id")


#CRUD OPERATION commands
session = Session(engine)

# add birthday
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.hybrid_command()
async def add(ctx, date=None, *, full_name: str):
        try:     
                
            sanitize_name = await sanitize_full_name(full_name, ctx)
            sanitize_dt = await sanitize_date(date, ctx)
            if sanitize_name and sanitize_dt:
                print(sanitize_name)
                await ctx.send(f"date: {sanitize_dt} , full_name: {sanitize_name}") 
                new_user = User(full_name=sanitize_name, date_of_birth=date)
                session.add(new_user)
                session.commit()
        except ValueError:
            await ctx.send("Write Date and full Name Correctly")

#fetch birthday
@bot.hybrid_command()
async def fetch(ctx):
    await ctx.send(f"""```json
{session.query(User).all()}```""")


#get user 
@bot.hybrid_command()
async def find(ctx:commands.Context,dt_pattern = date_pattern,f_name_pattern = full_name_pattern,*, arg: str):
    
    sanitize_arg = str(arg).replace("'","").replace('"','') 
    if re.match(dt_pattern,sanitize_arg):
        
        users = session.query(User).filter_by(date_of_birth =sanitize_arg).all()
        await ctx.send(f"""```json
{str(users)}```""")
    
    elif re.match(f_name_pattern,sanitize_arg):
        users = session.query(User).filter_by(full_name=sanitize_arg).all()
        await ctx.send(f"""```json
{str(users)}```""")
    else:
        await ctx.send("Wrong argument couldn't find anyone.")
#Update User

@bot.hybrid_command()
async def update(ctx:commands.Context,id:str , *, arg:str , dt_pattern = date_pattern , f_name_pattern = full_name_pattern):
    
    s_id = await sanitize_id(id, ctx)

    sanitize_arg = str(arg).replace("'","").replace('"','')
    
    user = session.query(User).filter_by(id=s_id).first()
    
    if re.match(dt_pattern, sanitize_arg):
        user.date_of_birth = sanitize_arg
        session.commit()
        await ctx.send("Updated User Info successfully.")


    elif re.match(f_name_pattern,sanitize_arg):
        user = session.query(User).filter_by(id=s_id).first()
        user.full_name = sanitize_arg
        session.commit()
        await ctx.send("Updated User Info successfully.")

    else:
        await ctx.send("Wrong argument couldn't find anyone.")


#delete User

@bot.hybrid_command()
async def delete(ctx:commands.Context,id: str):
    

    s_id = await sanitize_id(id, ctx)
    user = session.query(User).filter_by(id=s_id).first() if s_id else False
    if user:
        session.delete(user)
        session.commit()
        await ctx.send(f" {user.full_name} deleted successfully.")
    else:
        await ctx.send(f" Wrong No User found")

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
   
