import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
client = commands.Bot(command_prefix = '$',intents=discord.Intents.all())


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.green)
    async def sed(self,  interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Hello SSup")

@client.command()
async def menu(ctx):
    view = Menu()
    await ctx.reply(view = view)


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.dnd, activity=discord.Game('Building!')) #Game/ Streaming(name = 'Minecraft', url = '')
    #await client.change_presence(status = discord.Status.dnd, activity=discord.Activity(type = discord.ActivityType.listening, name = 'some text'))
    await load_extensions()
    print("PaxMax is functioning properly!!!")
    print('---------------------------------')
    print(f"User : {client.user} (ID : {client.user.id})")
    print(f"Guild ID : {client.guilds[0].id}")
    print('---------------------------------')
    GUILDS_ID = discord.Object(id = int(os.getenv("GUILD")))
    
    client.tree.copy_global_to(guild=GUILDS_ID)
    try :
        synced = await client.tree.sync(guild=GUILDS_ID)
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)


@client.hybrid_command(name='say', description='Make the bot send messages!')
async def say(interaction: discord.Interaction, text: str):
    await interaction.send(content=text, ephemeral=True)

@client.tree.command(name="hello")
async def test(interaction : discord.Interaction):
    await interaction.response.send_message("Wow")
    
@client.tree.command(name="again")
async def test(interaction : discord.Interaction):
    await interaction.response.send_message("sheesh")

## ----------------------- Tests Required --------------------------

@client.tree.context_menu(name = "Show Join Date")
async def get_joined_date(interaction : discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"Member Joined : {discord.utils.format_dt(member.joined_at)} ", ephemeral = True)

@client.hybrid_command(name='report_message')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(f"Message Reported", ephemeral=True)

## ----------------------- ^ Required ^ ---------------------------
    

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
   