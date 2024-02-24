import discord
from discord.ext import commands


## Working, Tested OK :THUMNS_UP:

class TempVoiceChannel(commands.Cog):
    
    temperory_channels = []
    temperory_categories  = []
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member,before :discord.VoiceState,after:discord.VoiceState ):
        possible_channel_name = f"{member.display_name} yapping"
        if after.channel.name == "temp":
            temp_channel = await after.channel.clone(name = possible_channel_name)
            await member.move_to(temp_channel)
            self.temperory_channels.append(temp_channel.id)
        
        if after.channel.name == 'teams':
            temporary_category =  await after.channel.guild.create_category(name = possible_channel_name)
            await temporary_category.create_text_channel(name = "disposible")
            temp_channel = await temporary_category.create_voice_channel(name = "disposible")
            await member.move_to(temp_channel)
            self.temperory_categories.append(temp_channel.id)
            
        if before.channel:
            if before.channel.id in self.temperory_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
            if before.channel.id in self.temperory_categories:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                    await before.channel.category.delete()
         

async def setup(client):
    await client.add_cog(TempVoiceChannel(client))