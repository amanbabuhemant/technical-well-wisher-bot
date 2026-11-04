from dotenv import load_dotenv
from datetime import datetime
from datetime import date
import asyncio
import tracemalloc
import discord
import os 
load_dotenv()
tracemalloc.start()

# Create instance of Client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


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
    channel = client.get_channel(1532599339614994444)
    print(channel)
    await wish(channel)

# recursive function of checking date for wishes
async def wish(channel): 
    today = datetime.now()    
    today = str(today.strftime("%m-%d"))
    if today == "11-04":
        print("Artizote Birthday")
        await channel.send("@ghostor._. kya nakli id banaty ho drift")
         
client.run(os.getenv("TOKEN"))
   






