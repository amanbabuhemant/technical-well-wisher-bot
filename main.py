
from dotenv import load_dotenv
from datetime import date
import asyncio
import tracemalloc

import discord
import os 
load_dotenv()
tracemalloc.start()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # if message.content.startswith('Birthday'):
    #     print(message)
    #     print(client.get_channel(1532599339614994444))
        

@client.event 
async def on_connect():

    await asyncio.sleep(5)
    channel = client.get_channel(1532599339614994444)
    print(channel)
    await channel.send("Jio Shadow")





# await message.channel.send('Happy Birthday ')
# async def on_timing():
#   await asyncio.sleep(10)  
#   print(date.today())

# async def main():
#     result = await on_timing()
#     if result == "2026-11-02":
#         channel.send('Arti hogya')
#         print('done')
#     print(channel)
        
client.run(os.getenv("TOKEN"))
   






