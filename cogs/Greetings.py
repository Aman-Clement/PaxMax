import discord
from discord.ext import commands
from discord import app_commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client
            
    # @app_commands.command(name="command-1",description="wow")
    # @app_commands.guilds(discord.Object(id=...))
    # async def my_command(self, interaction: discord.Interaction) -> None:
    #     await interaction.response.send_message("Hello from command 1!", ephemeral=True)
    @commands.hybrid_command(name='what', description='Make the bot send messages!')
    async def what(self,interaction: discord.Interaction, text: str):
        await interaction.send(content=text, ephemeral=True)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello ! wassyuyp my N")
    
    @commands.command()
    async def message(self, ctx, user: discord.Member, *, message = None ):
        message = 'Welcome to the Server'
        embed = discord.Embed(title = message)
        await user.send(embed = embed)
    
    @commands.command()
    async def on_member_join(self,member):
        #the number is the channel ID
        #TODO : Add embed
        channel = self.client.get_channel(1197227352162312274)
        await channel.send('Hello!!!!')
        # await member.send('text')

    @commands.command()
    async def on_member_remove(self,member):
        #the number is the channel ID
        channel = self.client.get_channel(1197227352162312274)
        await channel.send('GoodBye!!!!')
    
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title = 'Dog', url = 'https://google.com', description = 'hmmm', color = 0x4dff4d)
        embed.set_author(name = ctx.author.display_name,url = 'https://wiki.com/', icon_url = ctx.author.avatar.url)
        embed.set_thumbnail(url = 'https://media.istockphoto.com/id/1494319570/photo/clouds-on-the-sky-sunset-weather.jpg?s=1024x1024&w=is&k=20&c=FvZr4yuju0kRG6239hPC4jMMzVRGkrSe8BLEIAufuGU=')
        embed.add_field(name = 'lab',value='below',inline=True)
        embed.add_field(name = 'labooo',value='belowoooo',inline=True)
        embed.set_footer(text='WOWOWO')
        await ctx.send(embed = embed )
        
    @commands.Cog.listener()
    async def on_member_join(self,ctx):
        embed = discord.Embed(title = ctx.display_name,color = 0x4dff4d)
        # embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        embed.set_thumbnail(url = ctx.avatar)
        embed.set_image(url='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN284ZDdraXloczdkOTUwcTU2dGtudGttb2VscDAwbTVndTh2YTVvdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l4FGpPki5v2Bcd6Ss/giphy-downsized-large.gif')
        embed.add_field(name = 'Joined Server',value=f'{discord.utils.format_dt(ctx.joined_at)}',inline=True)
        embed.add_field(name = 'Joined Discord',value=f'{discord.utils.format_dt(ctx.created_at)}',inline=True)
        embed.add_field(name = 'Welcome')
        channel = self.client.get_channel(1210901142989447188)
        await channel.send(embed = embed )
        # await member.send('text')
    
    @commands.command()
    async def checkout(self,ctx,member:discord.Member):
        embed = discord.Embed(title = member.display_name,color = 0x4dff4d)
        # embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar.url)
        embed.set_thumbnail(url = member.avatar)
        embed.add_field(name = 'Joined Server',value=f'{discord.utils.format_dt(member.joined_at)}',inline=True)
        embed.add_field(name = 'Joined Discord',value=f'{discord.utils.format_dt(member.created_at)}',inline=True)
        embed.add_field(name = 'DOB',value='will be added"',inline=False)
        embed.set_footer(text='')
        await ctx.send(embed = embed )
        # channel = self.client.get_channel(1197227352162312274)
        # await channel.send('Hello!!!!')
        # # await member.send('text')
    
    #Reactions
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user:
            return 
        channel = reaction.message.channel
        await channel.send(user.name + ' added' + reaction.emoji)
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user == self.client.user:
            return 
        channel = reaction.message.channel
        await channel.send(user.name + ' removed' + reaction.emoji)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author == self.client.user:
            return 
        if ('react') in message.content:
            emoji = '🥸'
            await message.add_reaction(emoji)

async def setup(client):
    await client.add_cog(Greetings(client), guilds = [discord.Object(id=1197227351319269487)])