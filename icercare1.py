import discord
from discord.errors import ClientException 
from discord.ext import commands

client = commands.Bot(command_prefix='*', intents=discord.Intents.all())



@client.event 
async def on_ready():
    general_channel = client.get_channel(912097369561104447)
    await general_channel.send("It is wednesday my dudes!")
    await general_channel.send("https://www.youtube.com/watch?v=du-TY1GUFGk")


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command(name='version')
async def version(context):
    myEmbed = discord.Embed(title="Curent Version", description="The bot is in Version 1.0", color= 0x5F57A9)
    myEmbed.add_field(name="Version Code:", value="v1.0.0", inline=False)
    myEmbed.add_field(name="Date released:", value="December 5, 2021", inline=False)
    myEmbed.set_footer(text="This is a sample")
    myEmbed.set_author(name="Matrix")
    await context.message.channel.send(embed=myEmbed)

@client.event
async def on_message(message):
    if message.content == 'opfgs':
        general_channel = client.get_channel(912097369561104447)

        myEmbed = discord.Embed(title="Curent Version", description="The bot is in Version 1.0", color= 0x5F57A9)
        myEmbed.add_field(name="Version Code:", value="v1.0.0", inline=False)
        myEmbed.add_field(name="Date released:", value="December 5, 2021", inline=False)
        myEmbed.set_footer(text="This is a sample")
        myEmbed.set_author(name="Matrix")

        await general_channel.send(embed=myEmbed)

    await client.process_commands(message)
    await client.change_presence(activity=discord.Streaming(name="Dumb shit", url="https://www.twitch.tv/spinigotilla"))
client.run('OTEyMDU0NzQwMjExMzYzOTEw.YZqXKw.T0BxYv2wjgLCS2rVht8IF9K3_n4')
