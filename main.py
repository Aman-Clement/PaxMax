import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import app_commands


load_dotenv()
client = commands.Bot(command_prefix = '$',intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.dnd, activity=discord.Game('Building!')) #Game/ Streaming(name = 'Minecraft', url = '')
    #await client.change_presence(status = discord.Status.dnd, activity=discord.Activity(type = discord.ActivityType.listening, name = 'some text'))
    await load_extensions()
    print("PaxMax is functioning properly!!!")
    print('---------------------------------')
    try :
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@client.tree.command(name="hello")
async def test(interaction : discord.Interaction):
    await interaction.response.send_message("Wow")
    
@client.tree.command(name="again")
async def test(interaction : discord.Interaction):
    await interaction.response.send_message("sheesh")

async def load_extensions():
    print("Loading extensions...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")
        else:
            print("Unable to load pycache folder.")
              
if __name__ == '__main__':        
    print("is it even working")
    Bot_Token = os.environ.get('BOT_TOKEN')
    client.run(Bot_Token)
   