import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, Member
from yt_dlp import YoutubeDL

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
        
        self.is_playing = False
        self.is_paused = False
        
        self.music_queue = []
        self.YDL_OPTIONS = {'format':'bestaudio','noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

        self.vc = None
    
    def searh_yt(self, song):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info('ytsearch:%s' %song, download= False)
            except Exception:
                return False
        first_result = info['entries'][0]  # Get the first search result
        return {'source': first_result['url'], 'title': first_result['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            print("here3?")
            self.is_playing = True
            
            m_url = self.music_queue[0][0]['source']
            
            self.music_queue.pop(0)
            
            audio_source = discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS)
            self.vc.play(audio_source, after= lambda e:self.play_next())
        else:
            self.is_playing = False
    
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            print("here?")
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                
                if self.vc is None:
                    await ctx.send("Could not connect to the VC")
                    return
            
            else:
                await self.vc.move_to(self.music_queue[0][1])

            
            print(m_url)
            audio_source = discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS)
            try:
                print("here2?")
                self.vc.play(audio_source, after=lambda e: self.play_next())
                await ctx.send("Now playing: " + self.music_queue[0][0]['title'])

            except Exception as e:
                print("An error occurred while playing the audio:", e)
                await ctx.send("An error occurred while playing the audio.")
                self.is_playing = False
        else:
            self.is_playing = False
            await ctx.send("The music queue is empty.")
        
    
    
    @commands.command(name = 'hit', aliases=['p','playing'], help = 'Play your banger')
    async def hit(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.searh_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. lawde incorrect format")
            else:
                await ctx.send('Song added to the queue')
                print([song, voice_channel])
                self.music_queue.append([song, voice_channel])
                print(self.music_queue)
                if self.is_playing == False:
                    await self.play_music(ctx)
                    
    
    @commands.command(name = 'hollup', help='Asks you to hollup')
    async def hollup(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()
    
    @commands.command(name = 'carryon', help='Asks you to hollup')
    async def carryon(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name = 'skipp', help='Asks you to hollup')
    async def skipp(self, ctx, *args):
        if self.vc!= None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
    
    @commands.command(name = 'qu', help='Asks you to hollup')
    async def qu(self, ctx):
        retval = ""
        
        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[0][1]['title'] +'\n'
        
        if retval != "":
            await ctx.send(retval)
        
        else:
            await ctx.send("No music")
    
    @commands.command(name = 'clear', help='Asks you to hollup')
    async def clear(self, ctx):
        if self.vc!=None and  self.is_playing :
            self.vc.stop()
        self.music_queue=[]
        await ctx.send("Music quque cleared")
    
    
    @commands.command()
    async def music_menu(self, ctx):
        view = self.create_music_menu(ctx)
        await ctx.reply("Music Menu:", view=view)

    def create_music_menu(self,ctx):
        class MusicMenu(discord.ui.View):
            def __init__(self,ctx,client):
                super().__init__()
                self.ctx = ctx
                self.client = client

            @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
            async def join(self,  interaction: discord.Interaction,  button: discord.ui.Button,):
                if(ctx.author.voice):
                    channel = ctx.message.author.voice.channel
                    voice = await channel.connect()
                    source = FFmpegPCMAudio('wave.wav')
                    player = voice.play(source)
                    await interaction.response.send_message("Joining...")
                else:
                    await interaction.response.send_message('You are not in a voice channel, You must be in a VC to run this command')

            @discord.ui.button(label="Leave", style=discord.ButtonStyle.red)
            async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
                if(self.ctx.voice_client):
                    await self.ctx.guild.voice_client.disconnect()
                    await interaction.response.send_message("Leaving...")
                else:
                    await interaction.response.send_message("I am not in a VC")

            @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
            async def skip(self, interaction: discord.Interaction, button: discord.ui.Button, ):
                voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
                voice.stop()  
                await interaction.response.send_message("Stopping...")

            @discord.ui.button(label="Resume", style=discord.ButtonStyle.grey)
            async def resume(self, button: discord.ui.Button, interaction: discord.Interaction):
                voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
                if voice.is_paused():
                    voice.resume()
                else:
                    await interaction.response.send_message('???? Resume what?')
                await interaction.response.send_message("Resuming...")

            @discord.ui.button(label="Pause", style=discord.ButtonStyle.blurple)
            async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
                voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
                if voice.is_playing():
                    voice.pause()
                else:
                    await ctx.send('???? pause what?')  

        return MusicMenu(ctx, self.client)
        
    @commands.command(pass_Context = True)
    async def join(self, ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('wave.wav')
            player = voice.play(source)
            view = self.create_music_menu(ctx)
            await ctx.reply("Music Menu:", view=view)
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
            view = self.create_music_menu(ctx)
            await ctx.reply("Music Menu:", view=view)
        else:
            await ctx.send('???? pause what?')
        

    @commands.command(pass_Context = True)
    async def resume(self,ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            view = self.create_music_menu(ctx)
            await ctx.reply("Music Menu:", view=view)
        else:
            await ctx.send('???? Resume what?')

    @commands.command(pass_Context = True)
    async def skip(self, ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        voice.stop()
        view = self.create_music_menu(ctx)
        await ctx.reply("Music Menu:", view=view)  

    @commands.command(pass_Context = True)
    async def play(self, ctx,arg):
        voice = ctx.guild.voice_client
        #change extension buddy
        source = FFmpegPCMAudio(arg) 
        player = voice.play(source, after = lambda x=None:check_queue(self,ctx,ctx.message.guild.id))

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