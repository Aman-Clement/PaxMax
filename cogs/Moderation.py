import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == 'fuck':
            await message.delete()
            await message.channel.send('Do that again and youll be banned')
        # await self.client.process_commands(message)
    
    @commands.command()
    @has_permissions(kick_members = True)
    async def kick(self, ctx,member: discord.Member, *, reason = None):
        await member.kick(reason = reason)
        await ctx.send(f'User {member} has been kicked')
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have permissions lil homie") 


    @commands.command()
    @has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f'User {member} has been banned')
    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have permissions for that lil homie") 

    @commands.command()
    @has_permissions(ban_members = True)
    async def unban(self, ctx, *, member_id: int):
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
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permissions for that lil homie')

async def setup(client):
    await client.add_cog(Moderation(client))