from enum import Enum

import discord
from discord.errors import ClientException 
from discord.ext import commands 
import random
import asyncio
import json

client = commands.Bot(command_prefix='*', intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="Dumb shit", url="https://www.twitch.tv/spinigotilla"))
    print("bot is ready")

@client.event
async def on_member_join(member):
    with open("/nice/autorole.json", "r") as f:
        role = json.load(f)
        fetched_role = discord.utils.get(member.guild.roles, name = role[str(member.guild.id)])
    
    await member.add_roles(fetched_role)

@client.command()
@commands.has_permissions(administrator=True)
async def setautorole(ctx, role: discord.Role):
    with open("/nice/autorole.json", "r") as f:
        mute_role = json.load(f)

        mute_role[str(ctx.guild.id)] = role.name

    with open("/nice/autorole.json", "w") as f:
        json.dump(mute_role, f, indent=4)
    
    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Autrole has been set!", value=f"The mute role has been changed to '{role.mention}' for this guild. All members wil have automaticaly equipped this role .", inline=False)

    await ctx.send(embed=conf_embed)


@client.event
async def on_guild_join(guild):
    with open("/bot/pateu/mute.json", "r") as f:
        mute_role = json.load(f)

        mute_role[str(guild.id)] = None

    with open("/bot/pateu/mute.json", "w") as f:
        json.dump(mute_role, f, indent=4)

@client.event
async def on_guild_remove(guild):
     with open("/bot/pateu/mute.json", "r") as f:
        mute_role = json.load(f)

        mute_role.pop(str(guild.id))

        with open("/bot/pateu/mute.json", "w") as f:
            json.dump(mute_role, f, indent=4)


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
    myEmbed.add_field(name="Date released:", value="March 09 , 2023", inline=False)
    myEmbed.set_footer(text="This is a sample")
    myEmbed.set_author(name="Matrix")
    await context.message.channel.send(embed=myEmbed)

@client.command(aliases=["8ball", "eight ball", "8 ball"])
async def eightball(ctx, *, question):
    with open("/nice/response.txt", "r") as f:
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

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a whole number in order to run")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, modreason):
    await ctx.guild.kick(member)

    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="kicked:", value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.", inline=False)
    conf_embed.add_field(name="Reason:", value=modreason, inline=False)

    await ctx.send(embed=conf_embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, modreason):
    await ctx.guild.ban(member)

    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Banned:", value=f"{member.mention} has been banned from the server by {ctx.author.mention}.", inline=False)
    conf_embed.add_field(name="Reason:", value=modreason, inline=False)
    
    await ctx.send(embed=conf_embed)

@client.command(name="unban")
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def unban(ctx, userId):
    user  = discord.Object(id=userId)
    await ctx.guild.unban(user)

    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Unbanned:", value=f"<@{userId}> has been unbanned from the server by {ctx.author.mention}.", inline=False)

    await ctx.send(embed=conf_embed)

@client.command()
@commands.has_permissions(administrator=True)
async def setmuterole(ctx, role: discord.Role):
    with open("/nice/mute.json", "r") as f:
        mute_role = json.load(f)

        mute_role[str(ctx.guild.id)] = role.name

    with open("/nice/mute.json", "w") as f:
        json.dump(mute_role, f, indent=4)
    
    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Mute role has been set!", value=f"The mute role has been changed to '{role.mention}' for this guild. All members are muted wil have automaticaly equipped this role .", inline=False)

    await ctx.send(embed=conf_embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, memeber: discord.Member):
    with open("/nice/mute.json", "r") as f:
        role = json.load(f)

        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])
    
    await memeber.add_roles(mute_role)  

    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Muted", value=f"{memeber.mention} has been muted by {ctx.author.mention}.", inline=False)

    await ctx.send(embed=conf_embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    with open("/nice/mute.json", "r") as f:
        role = json.load(f)
        
        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])
 
    await member.remove_roles(mute_role)
 
    conf_embed = discord.Embed(title="Success!", color=0x5F57A9)
    conf_embed.add_field(name="Unmuted", value=f"{member.mention} has been unmuted by {ctx.author.mention}.", inline=False)

    await ctx.send(embed=conf_embed)

@kick.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a user ID or a @ mention to run the kick command.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a user ID or a @ mention to run the ban command.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a user ID or a @ mention to run the unban command.")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a @ mention in order to run")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a @ mention in order to run")


client.run('OTEyMDU0NzQwMjExMzYzOTEw.YZqXKw.T0BxYv2wjgLCS2rVht8IF9K3_n4')