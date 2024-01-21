import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import FFmpegPCMAudio, Member



client = commands.Bot(command_prefix = '$',intents=discord.Intents.all())
load_dotenv()

#server --- song dictionary, bot can be part of many servers
queues = {}

def check_queue(ctx,id):
    if queues[id] != []:
        print("hello")
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.dnd, activity=discord.Game('Building!')) #Game/ Streaming(name = 'Minecraft', url = '')
    #await client.change_presence(status = discord.Status.dnd, activity=discord.Activity(type = discord.ActivityType.listening, name = 'some text'))
    
    print("PaxMax is functioning properly!!!")
    print('---------------------------------')

@client.command()
async def hello(ctx):
    await ctx.send("Hey, Wassup my N")

@client.event
async def on_member_join(member):
    #the number is the channel ID
    #TODO : Add embed
    channel = client.get_channel(1197227352162312274)
    await channel.send('Hello!!!!')
    # await member.send('text')

@client.event
async def on_member_remove(member):
    #the number is the channel ID
    channel = client.get_channel(1197227352162312274)
    await channel.send('GoodBye!!!!')
    

@client.command(pass_Context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('wave.wav')
        player = voice.play(source)
    else:
        await ctx.send('You are not in a voice channel, You must be in a VC to run this command')

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the VC")
    else:
        await ctx.send("I am not in a VC")
        
@client.command(pass_Context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('???? pause what?')  

@client.command(pass_Context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('???? Resume what?')

@client.command(pass_Context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()  

@client.command(pass_Context = True)
async def play(ctx,arg):
    voice = ctx.guild.voice_client
    #change extension buddy
    source = FFmpegPCMAudio(arg) 
    player = voice.play(source, after = lambda x=None:check_queue(ctx,ctx.message.guild.id))

@client.command(pass_Context = True)
async def queue(ctx,arg):
    voice = ctx.guild.voice_client
    #change extension buddy
    source = FFmpegPCMAudio(arg) 
    
    guild_id = ctx.message.guild.id
    
    if guild_id in queues:
        queues[guild_id].append(source)
    
    else:
        queues[guild_id] =[source]
        
    await ctx.send("Added to Queue")

#event
@client.event
async def on_message(message):
    if message.content == 'fuck':
        await message.delete()
        await message.channel.send('Do that again and youll be banned')
    await client.process_commands(message)
    
@client.command()
@has_permissions(kick_members = True)
async def kick(ctx,member: discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'User {member} has been kicked')
@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You do not have permissions lil homie") 


@client.command()
@has_permissions(ban_members = True)
async def ban(ctx,member: discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has been banned')
@ban.error
async def ban_error(ctx, error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You do not have permissions for that lil homie") 

@client.command()
@has_permissions(ban_members = True)
async def unban(ctx, *, member_id: int):
    bans = [entry async for entry in ctx.guild.bans(limit=2000)]
    for ban_entry in bans:
        user = ban_entry.user
        if user.id == member_id:
            await ctx.guild.unban(user)
            await ctx.send(f'User {user} has been unbanned.')
            return
        else:
            await ctx.send(f'User with ID {member_id} is not currently banned.')
        
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permissions for that lil homie')

@client.command()
async def embed(ctx):
    embed = discord.Embed(title = 'Dog', url = 'https://google.com', description = 'hmmm', color = 0x4dff4d)
    embed.set_author(name = ctx.author.display_name,url = 'https://wiki.com/', icon_url = ctx.author.avatar.url)
    embed.set_thumbnail(url = 'https://media.istockphoto.com/id/1494319570/photo/clouds-on-the-sky-sunset-weather.jpg?s=1024x1024&w=is&k=20&c=FvZr4yuju0kRG6239hPC4jMMzVRGkrSe8BLEIAufuGU=')
    embed.add_field(name = 'lab',value='below',inline=True)
    embed.add_field(name = 'labooo',value='belowoooo',inline=True)
    embed.set_footer(text='WOWOWO')
    await ctx.send(embed = embed )
    
@client.command()
async def message(ctx, user: discord.Member, *, message = None ):
    message = 'Welcome to the Server'
    embed = discord.Embed(title = message)
    await user.send(embed = embed)
      
#Error handling for any command
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingPermissions):
#         await ctx.send('You cannot do that')
        
                
Bot_Token = os.environ.get('BOT_TOKEN')
client.run(Bot_Token)    
