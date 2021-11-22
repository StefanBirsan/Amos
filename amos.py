import discord
from discord.errors import ClientException 

client = discord.Client()

@client.event 
async def on_ready():
    general_channel = client.get_channel(912097369561104447)
    await general_channel.send("It is wednesday my dudes!")
    await general_channel.send("https://www.youtube.com/watch?v=du-TY1GUFGk")
@client.event
async def on_disconnect():
    general_channel = client.get_channel(912097369561104447)
    await general_channel.send("Ya ya !")
@client.event
async def on_message(message):
    if message.content == 'what is the version':
        general_channel = client.get_channel(912097369561104447)
        await general_channel.send("The version is 1.0")

client.run('OTEyMDU0NzQwMjExMzYzOTEw.YZqXKw.T0BxYv2wjgLCS2rVht8IF9K3_n4')