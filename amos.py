import discord
from discord.errors import ClientException 
from discord.ext import commands 
from discord.utils import get
import random
import asyncio
import json
import aiohttp
import rule34
import urllib.request as u
import xml.etree.ElementTree as et
import discord.ui
from PIL import Image
import requests
from emojify import emojify_image
from typing import Union


client = commands.Bot(command_prefix='*', intents=discord.Intents.all())

client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="Dumb shit", url="https://www.twitch.tv/spinigotilla"))
    print("bot is ready")

@client.event
async def on_raw_reaction_add(reaction):
     if reaction.message_id == 1101572333430386688:
          if str(reaction.emoji) == "👍":
               verified_role = get(reaction.member.guild.roles, name="18+")
               await reaction.member.add_roles(verified_role)

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
    conf_embed.add_field(name="Autrole has been set!", value=f"The role has been changed to '{role.mention}' for this guild. All members wil have automaticaly equipped this role .", inline=False)

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

@client.command(name='version', aliases = ['botversion', 'bversion'])
async def version(ctx):
    myEmbed = discord.Embed(title="Curent Version", description="The bot is in Version 1.6", color= 0x5F57A9,  timestamp= ctx.message.created_at)
    myEmbed.add_field(name="Version Code:", value="v1.6.3", inline=False)
    myEmbed.add_field(name="Date released:", value="January 23, 2023", inline=False)
    myEmbed.add_field(name="Current version date release:", value="April 29, 2023", inline=False)
    myEmbed.set_footer(text="This is a sample")
    myEmbed.set_author(name="(Matrix)")
    myEmbed.set_footer(text=f"Requested by @{ctx.author}.", icon_url=ctx.author.avatar)
    await ctx.message.channel.send(embed=myEmbed)

#math

@client.command(aliases=['calculate'])
async def math(ctx, expression):
    symbols = ['+', '-' , '/', '*', '%']
    if any(s in expression for s in symbols):
        calculated = eval(expression)
        embed = discord.Embed(title="Math Expression", description=f"`Expression` {expression}\n`Answer` {calculated}", color= 0x5F57A9, timestamp=ctx.message.created_at)
    else:
        await ctx.send("This isn't a math problem")
    await ctx.send(embed=embed)

#dice

@client.command(aliases=['dice'])
async def roll(ctx, max:int=6):
    number = random.randint(1,max)
    await ctx.send(number)
    

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
    help_embed.add_field(name="Balance", value="Shows you how much money you got.", inline= False)
    help_embed.add_field(name="Begg", value="Make some money by begging.", inline= False)
    help_embed.add_field(name="User info", value="Show's the user's info ofc.", inline= False)
    help_embed.set_footer(text=f"Requested by @{ctx.author}.", icon_url=ctx.author.avatar)

    await ctx.send(embed=help_embed)

@client.command(aliases=['uinfo'])
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member
    
    roles = [role for role in member.roles]
    info_embed = discord.Embed(title=f"{member.name}'s User information", description=f"All information on user {member.mention}.", color= 0x5F57A9, timestamp= ctx.message.created_at)
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name="Name: ", value=member.name, inline=False)
    info_embed.add_field(name="Nick name:  ", value=member.display_name)
    info_embed.add_field(name="Created at", value= member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    info_embed.add_field(name="Discriminator: ", value=member.discriminator, inline=False)
    info_embed.add_field(name="ID: ", value=member.id, inline=False)
    info_embed.add_field(name=f"Roles ({len(roles)})  ", value=" ".join([role.mention for role in roles]))
    info_embed.add_field(name="Top Role:  ", value=member.top_role.mention, inline=False)
    info_embed.add_field(name="Joined at: ", value=member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    info_embed.add_field(name="Status: ", value=member.status, inline=False)
    

    await ctx.send(embed=info_embed)

@client.command(aliases=['svinfo', 'svinf'])
async def serverinfo(ctx):
    embed = discord.Embed(title="Server info", description=f"Here's the info on the server, {ctx.guild.name}.", color= 0x5F57A9, timestamp= ctx.message.created_at)
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name="Name", value= ctx.guild.name, inline=False)
    embed.add_field(name="ID", value= ctx.guild.id, inline=False)
    embed.add_field(name="Owner", value= ctx.guild.owner.mention, inline=False)
    embed.add_field(name="Members", value= ctx.guild.member_count)
    embed.add_field(name="Channels", value= f"{len(ctx.guild.text_channels)} text | {len(ctx.guild.voice_channels)} voice | {len(ctx.guild.stage_channels)} stages", inline=False)
    embed.add_field(name="Role Count", value= len(ctx.guild.roles), inline=False)
    embed.add_field(name="Rules Channel", value= ctx.guild.rules_channel, inline=False)
    embed.add_field(name="Premium boosts: ", value= ctx.guild.premium_subscription_count)
    embed.add_field(name="Booster Tier", value= ctx.guild.premium_tier, inline= False)
    embed.add_field(name="Created at: " , value= ctx.guild.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"), inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)

    await ctx.send(embed=embed)


#banned_words = ["FUCK"]

# @client.event
# async def on_message(message):
#     for word in banned_words:
#         if word in message.content.lower() or word in message.content.upper():
#             await message.delete()
#             await message.channel.send(f"{message.author.mention} You cannot say that word!")

#meme command

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cd:
        async with cd.get("https://www.reddit.com/r/memes.json") as r:
            memes = await r.json()
            embed = discord.Embed(color= 0x5F57A9)
            embed.set_image(url=memes["data"]["children"][random.randint(0, 40)]["data"]["url"])
            embed.set_footer(text=f"Meme send by {ctx.author}")

            await ctx.send(embed = embed)

@client.command()
async def emojify(ctx, url: Union[discord.Member, str], size: int = 14):
    if not isinstance(url, str):
        url = url.display_avatar.url

    def get_emojified_image():
        r = requests.get(url, stream=True)
        image = Image.open(r.raw).convert("RGB")
        res = emojify_image(image, size)

        if size > 14:
            res = f"```{res}```"
        return res

    result = await client.loop.run_in_executor(None, get_emojified_image)
    await ctx.send(result)

#cat command

@client.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as cd:
        async with cd.get("https://www.reddit.com/r/cats.json") as r:
            memes = await r.json()
            embed = discord.Embed(color= 0x5F57A9)
            embed.set_image(url=memes["data"]["children"][random.randint(0, 40)]["data"]["url"])
            embed.set_footer(text=f"Meme send by {ctx.author}")

            await ctx.send(embed = embed)

#horny command

r = rule34.Rule34
def xmlparse(str):
	root = et.parse(u.urlopen(str))
	for i in root.iter('post'):
		fileurl = i.attrib['file_url']
		return fileurl
def xmlcount(str):
	root = et.parse(u.urlopen(str))
	for i in root.iter('posts'):
		count = i.attrib['count']
		return count
def pidfix(str):
	ye = int(xmlcount(r.urlGen(tags=str,limit=1)))
	ye = ye - 1
	return ye
def rdl(str,int):
	

	if int > 2000:
		int = 2000
	if int == 0:
		int == 0
		
	elif int != 0:	
		int = random.randint(1,int)
	
	xurl = r.urlGen(tags=str,limit=1,PID=int)
	print(xurl)
	wr = xmlparse(xurl)
	
	if 'webm' in wr:
		if 'sound' not in str:
			if 'webm' not in str:
				
				wr = rdl(str,pidfix(str))
		else:
			pass
	elif 'webm' not in wr:
		print('pateu')
	return wr

@client.command()
async def pl(ctx, * ,arg):
	answer = ''
	# this is inefficent but also the only way i can do this
	arg = str(arg)
	arg = arg.replace(',','')
	arg = arg.replace('(','')
	arg = arg.replace(')','')
	arg = arg.replace("'",'')
	
	waitone = await ctx.send("***:desktop: We're polling Rule34! Please wait a few seconds.***")
	newint = pidfix(arg)
	if newint > 2000:
		newint = 2000
		answer = rdl(arg,random.randint(1,newint))
	if newint > 1:

		answer = rdl(arg,random.randint(1,newint))
	elif newint < 1:
		if newint == 0:
			answer = rdl(arg,0)
		elif newint != 0:
			answer = rdl(arg,1)
   
	if 'webm' in answer:
		await waitone.delete
		await ctx.send(answer)
	elif 'webm' not in answer:
		embed = discord.Embed(title=f'Rule34: {arg}',color=ctx.author.color)
		embed.set_author(name=f'{ctx.author.display_name}')
		embed.set_thumbnail(url='https://rule34.paheal.net/themes/rule34v2/rule34_logo_top.png')
		embed.set_image(url=f'{answer}')
		waitone.delete
		await ctx.send(embed = embed)

#crypto

@client.command()
async def balance(ctx, member: discord.Member=None):
    with open("/bot/pateu/eco.json", "r") as f:
        user_eco = json.load(f)
    
    if member is None:
        member = ctx.author
    elif member is not None:
        member = member
    
    if str(member.id) not in user_eco:

        user_eco[str(ctx.author.id)] = {}
        user_eco[str(ctx.author.id)]["Balance"] = 100
        user_eco[str(ctx.author.id)]["Deposited"] = 0

        with open("/bot/pateu/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    eco_embed = discord.Embed(title=f"{member.name}'s current balance", description="The curent balance of this user.", color= 0x5F57A9)
    eco_embed.add_field(name="Current balance:", value=f"${user_eco[str(member.id)]['Balance']}.", inline= False)
    eco_embed.add_field(name="Bank Balance:", value=f"${user_eco[str(member.id)]['Deposited']}.")
    eco_embed.set_footer(text="Want to increase balance? Try running some economy based commands!", icon_url=None)

    await ctx.send(embed=eco_embed)


@client.command()
async def begg(ctx):
    with open("/bot/pateu/eco.json", "r") as f:
        user_eco = json.load(f)
    
    if str(ctx.author.id) not in user_eco:
        user_eco[str(ctx.author.id)] = {}
        user_eco[str(ctx.author.id)]["Balance"] = 100
        user_eco[str(ctx.author.id)]["Deposited"] = 0

        with open("/bot/pateu/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    cur_bal = user_eco[str(ctx.author.id)]["Balance"]
    amount = random.randint(-10, 30)
    new_bal = cur_bal + amount

    if cur_bal > new_bal:
        
        eco_embed = discord.Embed(title="OH NO!", description="A group of robbers saw opportunity and took advantage of you", color= 0x5F57A9)
        eco_embed.add_field(name="New balance:", value=f"${new_bal}", inline=False)
        eco_embed.set_footer(text="Should probably beg in a nicer part of town..", icon_url=None)

        await ctx.send(embed=eco_embed)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("/bot/pateu/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)


    elif cur_bal < new_bal:

        eco_embed = discord.Embed(title="Oh lucky you!", description="Some kind soul has given you what they could.", color= 0x5F57A9)
        eco_embed.add_field(name="New balance:", value=f"${new_bal}", inline= False)
        eco_embed.set_footer(text="Want more? Try other commands too!", icon_url= None)
        await ctx.send(embed=eco_embed)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("/bot/pateu/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    
    elif cur_bal == new_bal:

        eco_embed = discord.Embed(title="Awh that sucks!", description="Looks like begging didn't help much..", color= 0x5F57A9)
        eco_embed.set_footer(text="Want more? Try some other commands too!")
        await ctx.send(embed=eco_embed)

@commands.cooldown(1, per=3600)
@client.command()
async def work(ctx):
     with open("/bot/pateu/eco.json", "r") as f:
        user_eco = json.load(f)

     if str(ctx.author.id) not in user_eco:
          
          user_eco[str(ctx.author.id)] = {}
          user_eco[str(ctx.author.id)]["Balance"] = 100
          user_eco[str(ctx.author.id)]["Deposited"] = 0

          with open("/bot/pateu/eco.json", "w") as f:
            json.dump(user_eco, f , indent=4)
    
     amount = random.randint(100, 300)
     user_eco[str(ctx.author.id)]["Balance"] += amount

     eco_embed = discord.Embed(title="Phew!", description="After a tiring shift, here is what you earned!", color= 0x5F57A9)
     eco_embed.add_field(name="Earnings:", value=f"${amount}", inline=False)
     eco_embed.add_field(name="New Balance:", value=f"${user_eco[str(ctx.author.id)]['Balance']}.")
     eco_embed.set_footer(text="Want more? wait 1 hour to run this command again, or try some others!", icon_url=None)
     
     await ctx.send(embed=eco_embed)
     
     with open("/bot/pateu/eco.json", "w") as f:
            json.dump(user_eco, f , indent=4)

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: You have to wait 1 hour.")

@client.command()
async def steal(ctx, member: discord.Member):
     with open("/bot/pateu/eco.json", "r") as f:
            user_eco = json.load(f)
     
     steal_probability = random.randint(0, 1)

     if steal_probability == 1:
          amount = random.randint(1, 100)

          if str(ctx.author.id) not in user_eco:
               
               if str(ctx.author.id) not in user_eco:
                 user_eco[str(ctx.author.id)] = {}
                 user_eco[str(ctx.author.id)]["Balance"] = 100
                 user_eco[str(ctx.author.id)]["Deposited"] = 0

               with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)

          elif str(member.id) not in user_eco:
               user_eco[str(ctx.author.id)] = {}
               user_eco[str(ctx.author.id)]["Balance"] = 100

               with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)
          
          user_eco[str(ctx.author.id)]["Balance"] += amount
          user_eco[str(member.id)]["Balance"] -= amount

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)
          
          await ctx.send(f"{ctx.author.mention}, You have stolen ${amount} from {member.mention}! Be sure to keep it safe!")
     
     elif steal_probability  == 0:
          await ctx.send("Uh oh.. You did not get to steal from this user.")

@client.command(aliases=["bank"])
async def deposit(ctx, amount: int):
     with open("/bot/pateu/eco.json", "r") as f:
        user_eco = json.load(f)
     
     if str(ctx.author.id) not in user_eco:
          user_eco[str(ctx.author.id)] = {}
          user_eco[str(ctx.author.id)]["Balance"] = 100
          user_eco[str(ctx.author.id)]["Deposited"] = 0

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)
     
     if amount > user_eco[str(ctx.author.id)]["Balance"]:
          await ctx.send("Cannot deposit this amount because your balance does not have the sufficient fonds.")
     else:
          user_eco[str(ctx.author.id)]["Deposited"] += amount
          user_eco[str(ctx.author.id)]["Balance"] -= amount
          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)
          
          await ctx.send(f"You have deposited ${amount} into your bank. This money is now safe and only you can touch it.")

@client.command(aliases=["wd"])
async def withdrawl(ctx, amount: int):
     with open("/bot/pateu/eco.json", "r") as f:
        user_eco = json.load(f)
     
     if str(ctx.author.id) not in user_eco:
          user_eco[str(ctx.author.id)] = {}
          user_eco[str(ctx.author.id)]["Balance"] = 100
          user_eco[str(ctx.author.id)]["Deposited"] = 0

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)
     
     if amount > user_eco[str(ctx.author.id)]["Deposited"]:
          await ctx.send("Cannot withdrawl this amount because your bank does not have it.")
     else:
          user_eco[str(ctx.author.id)]["Deposited"] -= amount
          user_eco[str(ctx.author.id)]["Balance"] += amount
          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)
          
          await ctx.send(f"You have withdrawn ${amount} into your bank. The money is no longer safe.")

@client.command(aliases=["flip"])
async def coinflip(ctx, amount: int, choice=None):
     with open("/bot/pateu/eco.json", "r") as f:
        user_eco = json.load(f)
     
     if str(ctx.author.id) not in user_eco:
          user_eco[str(ctx.author.id)] = {}
          user_eco[str(ctx.author.id)]["Balance"] = 100
          user_eco[str(ctx.author.id)]["Deposited"] = 0

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)

     if choice == None or choice != 'heads' and choice != 'tails':
          await ctx.send("Please enter a valid choice!")
          return
     computer_choice = random.randint(1, 2)
     if computer_choice == 1 and choice == 'heads':
          amount = (amount * 2 + 90) // 3
          user_eco[str(ctx.author.id)]["Balance"] += amount

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)

          await ctx.send(f"You won ${amount}! The coin landed on **HEADS**")

     elif computer_choice == 2 and choice == 'tails':
          amount = (amount * 2 + 90) // 3
          user_eco[str(ctx.author.id)]["Balance"] += amount 

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)

          await ctx.send(f"You won ${amount}! The coin landed on **TAILS**")       
     else:
          if computer_choice == 1:
               choice = 'HEADS'
          else:
               choice = 'TAILS'
          user_eco[str(ctx.author.id)]["Balance"] -= amount

          with open("/bot/pateu/eco.json", "w") as f:
                 json.dump(user_eco, f , indent=4)

          await ctx.send(f"You lost {amount}.. The coin landed on **{choice}**")            

client.run('OTEyMDU0NzQwMjExMzYzOTEw.GHIEW4.oEiNFn7_fpxK0-aSUo3KeZfwEePOuxiXCjmuyM')