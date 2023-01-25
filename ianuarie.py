import discord
from discord.errors import ClientException 
from discord.ext import commands 
import random
import asyncio

client = commands.Bot(command_prefix='*', intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="Dumb shit", url="https://www.twitch.tv/spinigotilla"))
    print("bot is ready")

@client.command()
async def ping(ctx):
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {bot_latency} ms.")

@client.command(aliases=["iloveyou"])
async def ily(ctx, *, why):
    with open("/bot/ilove.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await ctx.send('one of the reasons why i love you:')
    await ctx.send(response)

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
    with open("/bot/response.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    
    await ctx.send(response)

@client.command()
async def purge(ctx, amount:int):
    if amount > 1000:
        await ctx.send(f"too many messages to search given ({amount}/1000)")
    else:
        count_members = {}
        messages = await ctx.channel.history(limit=amount).flatten()
        for message in messages:
            if str(message.author) in count_members:
                count_members[str(message.author)] += 1
            else:
                count_members[str(message.author)] = 1
            
        new_string = []
        message_deleted = 0
        for author, message_deleted in list(count_members.items()):
            new_string.append(f'**{author}**: {message_deleted}')
            message_deleted += message_deleted
        final_string = '\n'.join(new_string)
        await ctx.channel.purge(limit=amount+1)
        msg = await ctx.send(f'{message_deleted} messages were removed. \n\n{final_string}')
        await asyncio.sleep(2)
        await msg.delete()

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason=None):
    if reason == None:
        reason="no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f"User {member.mention} has been kicked for {reason}")


client.run('OTEyMDU0NzQwMjExMzYzOTEw.YZqXKw.T0BxYv2wjgLCS2rVht8IF9K3_n4')
