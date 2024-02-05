import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, Member

queues = {}


def check_queue(self, ctx,id):
    if queues[id] != []:
        print("hello")
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    
    @commands.command()
    async def music_menu(self, ctx):
        view = self.create_music_menu(ctx)
        await ctx.reply("Music Menu:", view=view)

    def create_music_menu(self,ctx):
        class MusicMenu(discord.ui.View):
            def __init__(self,ctx):
                super().__init__()
                self.ctx = ctx

            @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
            async def join(self, button: discord.ui.Button, interaction: discord.Interaction):
                await interaction.response.send_message("Joining...")

            @discord.ui.button(label="Leave", style=discord.ButtonStyle.red)
            async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
                if(self.ctx.voice_client):
                    await self.ctx.guild.voice_client.disconnect()
                    await interaction.response.send_message("Leaving...")
                else:
                    await interaction.response.send_message("I am not in a VC")

            @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
            async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
                await interaction.response.send_message("Stopping...")

            @discord.ui.button(label="Resume", style=discord.ButtonStyle.grey)
            async def resume(self, button: discord.ui.Button, interaction: discord.Interaction):
                await interaction.response.send_message("Resuming...")

            @discord.ui.button(label="Pause", style=discord.ButtonStyle.blurple)
            async def pause(self, button: discord.ui.Button, interaction: discord.Interaction):
                await interaction.response.send_message("Pausing...")

        return MusicMenu(ctx)
        
    @commands.command(pass_Context = True)
    async def join(self, ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('wave.wav')
            player = voice.play(source)
        else:
            await ctx.send('You are not in a voice channel, You must be in a VC to run this command')

    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I left the VC")
        else:
            await ctx.send("I am not in a VC")
            
    @commands.command(pass_Context = True)
    async def pause(self,ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('???? pause what?')  

    @commands.command(pass_Context = True)
    async def resume(self,ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('???? Resume what?')

    @commands.command(pass_Context = True)
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        voice.stop()  

    @commands.command(pass_Context = True)
    async def play(self, ctx,arg):
        voice = ctx.guild.voice_client
        #change extension buddy
        source = FFmpegPCMAudio(arg) 
        player = voice.play(source, after = lambda x=None:check_queue(ctx,ctx.message.guild.id))

    @commands.command(pass_Context = True)
    async def queue(self, ctx, arg):
        voice = ctx.guild.voice_client
        #change extension buddy
        source = FFmpegPCMAudio(arg) 
        
        guild_id = ctx.message.guild.id
        
        if guild_id in queues:
            queues[guild_id].append(source)
        
        else:
            queues[guild_id] =[source]
            
        await ctx.send("Added to Queue")

async def setup(client):
    await client.add_cog(Music(client))