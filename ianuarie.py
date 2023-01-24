import discord
from discord.errors import ClientException 
from discord.ext import commands
import random

client = commands.Bot(command_prefix='*', intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="Dumb shit", url="https://www.twitch.tv/spinigotilla"))
    print("bot is ready")

@client.command()
async def ping(ctx):
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {bot_latency} ms.")

@client.command()
async def ily(ctx):
    await ctx.send("I love Mara!")

@client.command(name='version')
async def version(context):
    myEmbed = discord.Embed(title="Curent Version", description="The bot is in Version 1.0", color= 0x5F57A9)
    myEmbed.add_field(name="Version Code:", value="v1.1.0", inline=False)
    myEmbed.add_field(name="Date released:", value="January 23, 2023", inline=False)
    myEmbed.set_footer(text="This is a sample")
    myEmbed.set_author(name="Matrix")
    await context.message.channel.send(embed=myEmbed)

@client.command(aliases=["8ball", "eight ball", "8 ball"])
async def eightball(ctx, *, question):
    with open("/amos/response.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    
    await ctx.send(response)

client.run('OTEyMDU0NzQwMjExMzYzOTEw.YZqXKw.T0BxYv2wjgLCS2rVht8IF9K3_n4')
