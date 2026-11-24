from sqlalchemy.orm import Session
import tracemalloc
import discord
from discord.ext import commands
from env import *
from database.models.user import User
from database.models import engine
from time import sleep
from utils import *
import io
import requests

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

session = Session(engine)

bot = commands.Bot(command_prefix='$', intents=intents)


#CRUD OPERATION commands

# add birthday
@bot.hybrid_command()
async def add(ctx, date: str = "",*, full_name: str = ""):
        try:     
            sanitized_name = sanitize_name(full_name)
            sanitized_date = sanitize_date(date)

            if not sanitized_date:
                await ctx.send("Write Date in Correct Format MM-DD")
                return

            if not sanitized_name:
                await ctx.send("Enter name correctly.")
                return

            if sanitized_name and sanitized_date:
                await ctx.send(f"date: {sanitized_date} , full_name: {sanitized_name}") 
                new_user = User(full_name=sanitized_name, date_of_birth=sanitized_date)
                session.add(new_user)
                session.commit()
        except:
            await ctx.send("Write Date and full Name Correctly")


#fetch birthday
@bot.hybrid_command()
async def fetch(ctx):
    users = session.query(User).all()

    rows_html = ""
    for user in users:
        rows_html += f"""
        <tr class="border-b border-gray-200 hover:bg-gray-50">
            <td class="py-3 px-6 text-left">{user.id}</td>
            <td class="py-3 px-6 text-left font-medium">{user.full_name}</td>
            <td class="py-3 px-6 text-left">{user.date_of_birth}</td>
        </tr>
        """
        
        html_content = f"""<html>
                <head>
                    <script src="https://cdn.tailwindcss.com"></script>
                </head>
                    <body>
                <div class="max-w-4xl mx-auto bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 bg-gray-800 text-white">
            <h1 class="text-xl font-bold">Birthday List</h1>
        </div>
        <table class="min-w-full leading-normal">
            <thead>
                <tr class="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                    <th class="py-3 px-6 text-left">ID</th>
                    <th class="py-3 px-6 text-left">Name</th>
                    <th class="py-3 px-6 text-left">Birthday</th>
                </tr>
            </thead>
            <tbody class="text-gray-700 text-sm">
                {rows_html}
            </tbody>
        </table>
    </div>
                </body>
                </html> """
        
    filename = "fetch.html"
    with open(filename, "w", encoding = "utf-8") as f:
                f.write(html_content)

    
    url = 'https://api.htmlify.me/v1/tmpfiles'
    payload = { 'name': filename, 'expiry': 100000  }
    
    with open(filename, "rb") as f:
         files = {"file": (filename, f, 'text/html')}
         print(f)
         r = requests.post(url, data=payload, files=files)

    # print(files)
    # sleep(0.6)

    data = r.json()
    link = data.get("url")
    await ctx.send(link)
    # await ctx.send("Here is the exported birthday table:", file=discord_file)

#get user 
@bot.hybrid_command()
async def find(ctx:commands.Context, arg: str):

    if sanitized_date := sanitize_date(arg):
        users = session.query(User).filter_by(date_of_birth =sanitized_date).all()
        users = session.query(User).all()
        for user in users:
            sleep(0.1)
            await ctx.send(user.to_json_snippet())
    
    elif sanitized_name := sanitize_name(arg):
        users = session.query(User).filter_by(full_name=sanitized_name).all()
        users = session.query(User).filter_by(date_of_birth =sanitized_date).all()
        users = session.query(User).all()
        for user in users:
            sleep(0.1)
            await ctx.send(user.to_json_snippet())

    else:
        await ctx.send("Wrong argument couldn't find anyone.")


#Update User
@bot.hybrid_command()
async def update(ctx:commands.Context,id:str , *, arg:str):
    
    s_id = sanitize_id(id)

    if not s_id:
        await ctx.send("ID is not valid.")
        return
    
    user = session.query(User).filter_by(id=s_id).first()
    
    if not user:
        await ctx.send("Record not found with this ID.")
        return
    
    if sanitized_date := sanitize_date(arg):
        user.date_of_birth = sanitized_date
        session.commit()
        await ctx.send("Updated User Info successfully.")

    elif sanitized_name := sanitize_name(arg):
        user.full_name = sanitized_name
        session.commit()
        await ctx.send("Updated User Info successfully.")

    else:
        await ctx.send("Wrong argument couldn't find anyone.")


#delete User
@bot.hybrid_command()
async def delete(ctx:commands.Context,id: str):
    

    s_id = sanitize_id(id)
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



# run bot and client

bot.run(TOKEN)

client.run(TOKEN)
   
