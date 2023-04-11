import discord
from discord.errors import ClientException 
from discord.ext import commands 
import random
import asyncio
import json


client = commands.Bot(command_prefix='*', intents=discord.Intents.all())

client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="Dumb shit", url="https://www.twitch.tv/spinigotilla"))
    print("bot is ready")

#de aici incepe autorole-u

@client.command()
@commands.has_permissions(administrator=True)
async def setautorole(ctx, role: discord.Role):
    with open("/bot/pateu/autorole.json", "r") as f:
        auto_role = json.load(f)

        auto_role[str(ctx.guild.id)] = role.name

    with open("/bot/pateu/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)
    
    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Autrole has been set!", value=f"The mute role has been changed to '{role.mention}' for this guild. All members wil have automaticaly equipped this role .", inline=False)

    await ctx.send(embed=conf_embed)


@client.event
async def on_guild_join(guild):
    with open("/bot/pateu/autorole.json", "r") as f:
        auto_role = json.load(f)

    auto_role[str(guild.id)] = None

    with open("bot/pateu/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("/bot/pateu/autorole.json", "r") as f:
        auto_role = json.load(f)

    auto_role.pop[str(guild.id)]

    with open("bot/pateu/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)

@client.event
async def on_member_join(member):
    with open("/bot/pateu/autorole.json", "r") as f:
        auto_role = json.load(f)

    join_role = discord.utils.get(member.guild.roles, name=auto_role[str(member.guild.id)])

    await member.add_roles(join_role)

#mai jos e mute 

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

#ping

@client.command()
async def ping(ctx):
    print("baka")
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {bot_latency} ms.")


#special comand 

@client.command(aliases=["iloveyou"])
async def ily(ctx, *, why):
    with open("/bot/ilove.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await ctx.send('one of the reasons why i love you:')
    await ctx.send(response)

#version :D

@client.command(name='version')
async def version(context):
    myEmbed = discord.Embed(title="Curent Version", description="The bot is in Version 1.0", color= 0x5F57A9)
    myEmbed.add_field(name="Version Code:", value="v1.1.0", inline=False)
    myEmbed.add_field(name="Date released:", value="January 23, 2023", inline=False)
    myEmbed.set_footer(text="This is a sample")
    myEmbed.set_author(name="Matrix")
    await context.message.channel.send(embed=myEmbed)

#8ball

@client.command(aliases=["8ball", "eight ball", "8 ball"])
async def eightball(ctx, *, question):
    with open("/bot/response.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    
    await ctx.send(response)

#purge

@client.command()
async def purge(ctx, amount:int):
    await ctx.channel.purge(limit=amount+1)
    msg = await ctx.send(f'{amount} messages were deleted. \n')
    await asyncio.sleep(3)
    await msg.delete()

#error handling     

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing argument. You must pass in a whole number in order to run")

#admin commands

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
    with open("/bot/pateu/mute.json", "r") as f:
        mute_role = json.load(f)

        mute_role[str(ctx.guild.id)] = role.name

    with open("/bot/pateu/mute.json", "w") as f:
        json.dump(mute_role, f, indent=4)
    
    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Mute role has been set!", value=f"The mute role has been changed to '{role.mention}' for this guild. All members are muted wil have automaticaly equipped this role .", inline=False)

    await ctx.send(embed=conf_embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, memeber: discord.Member):
    with open("/bot/pateu/mute.json", "r") as f:
        role = json.load(f)

        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])
    
    await memeber.add_roles(mute_role)  

    conf_embed = discord.Embed(title="Success!", color= 0x5F57A9)
    conf_embed.add_field(name="Muted", value=f"{memeber.mention} has been muted by {ctx.author.mention}.", inline=False)

    await ctx.send(embed=conf_embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    with open("/bot/pateu/mute.json", "r") as f:
        role = json.load(f)
        
        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])
 
    await member.remove_roles(mute_role)
 
    conf_embed = discord.Embed(title="Success!", color=0x5F57A9)
    conf_embed.add_field(name="Unmuted", value=f"{member.mention} has been unmuted by {ctx.author.mention}.", inline=False)

    await ctx.send(embed=conf_embed)

#error handling x2

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

#help command

@client.command()
async def help(ctx):
    help_embed = discord.Embed(title="Help desk for Amos", description="All commands in one place", color=0x5F57A9)

    help_embed.set_author(name="Amos")
    help_embed.add_field(name="Purge", value="Kills a number of messages :D ", inline=False)
    help_embed.add_field(name="8ball", value="Ask and u might get an answear", inline=False)
    help_embed.add_field(name="Kick", value="I wonder this does.. hmm..", inline=False)
    help_embed.add_field(name="Ban", value="I guess you know what this does right?", inline=False)
    help_embed.add_field(name="Unban" , value="Unban yo homie" , inline=False)
    help_embed.set_footer(text=f"Requested by @{ctx.author}.", icon_url=ctx.author.avatar)

    await ctx.send(embed=help_embed)

@client.command()
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member
    
    info_embed = discord.Embed(title=f"{member.name}'s User information", description="All information about this user.", color=0x5F57A9)
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name="Name: ", value=member.name, inline=False)
    info_embed.add_field(name="Nick name: ", value=member.display_name, inline=False)
    info_embed.add_field(name="Discriminator: ", value=member.discriminator, inline=False)
    info_embed.add_field(name="ID: ", value=member.id, inline=False)
    info_embed.add_field(name="Top Role: ", value=member.top_role, inline=False)
    info_embed.add_field(name="Status: ", value=member.status, inline=False)
    

    await ctx.send(embed=info_embed)

#banned_words = ["FUCK"]

# @client.event
# async def on_message(message):
#     for word in banned_words:
#         if word in message.content.lower() or word in message.content.upper():
#             await message.delete()
#             await message.channel.send(f"{message.author.mention} You cannot say that word!")

client.run('OTEyMDU0NzQwMjExMzYzOTEw.YZqXKw.T0BxYv2wjgLCS2rVht8IF9K3_n4')
