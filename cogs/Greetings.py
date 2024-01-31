import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client
    
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

async def setup(client):
    await client.add_cog(Greetings(client))