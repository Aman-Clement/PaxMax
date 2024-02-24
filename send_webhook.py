import asyncio
import discord
from discord import Webhook
import aiohttp

async def sending(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session = session)
        embed = discord.Embed(title=" Test Test Test")
        await webhook.send(embed = embed , username = "Captain Cooking")
    
if __name__ == "__main__":
    url = "https://discord.com/api/webhooks/1210832232617484288/i7GZwEmCfEYNWUnoihoXSqNtfW-N5JYKT7nPFScYVal3sbGw1Plh8BzIX4veYhDqCTfj"
   
    loop = asyncio.new_event_loop()
    loop.run_until_complete(sending(url))
    loop.close()  
    


# COMMENTS : SUCCESS !))% WORKING