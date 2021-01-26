import discord
from discord.ext import commands, tasks
import sys, traceback
from itertools import cycle
import random
import asyncio
import yaml

intents = discord.Intents.default()
intents.members = True

config = yaml.load(open("settings/settings.yaml"))

def get_prefix(bot, message):
    prefixes = ['>']
    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.onmemberjoin', 'cogs.usercommands']

bot = commands.Bot(command_prefix=get_prefix, description='testing', intents=intents)
bot.remove_command('help')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    matchme.start()
    conversationstarter.start()
    presencenummatched.start()
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\ndiscord.py Version: {discord.__version__}\n')
    print(f'Logged in, run it up!')

@tasks.loop(seconds=3)
async def matchme():
    memberlist = []
    guild = bot.get_guild(config["serverid"])
    for member in guild.members:
        if discord.utils.get(guild.roles, name="Matching") in member.roles:
            memberlist.append(member)
    if len(memberlist) >= 2:
        member1 = memberlist[0]
        member2 = memberlist[1]
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            guild.get_member(member1.id): discord.PermissionOverwrite(read_messages=True),
            guild.get_member(member2.id): discord.PermissionOverwrite(read_messages=True)
        }
        overwritesvoice = {
            guild.default_role: discord.PermissionOverwrite(connect=False),
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(connect=True),
            guild.me: discord.PermissionOverwrite(view_channel=True),
            guild.get_member(member1.id): discord.PermissionOverwrite(connect=True),
            guild.get_member(member2.id): discord.PermissionOverwrite(connect=True),
            guild.get_member(member1.id): discord.PermissionOverwrite(view_channel=True),
            guild.get_member(member2.id): discord.PermissionOverwrite(view_channel=True)

        }
        textchannel = await guild.create_text_channel("Matched With User", overwrites=overwrites, user_limit=2)
        await guild.create_voice_channel("Matched With User", overwrites=overwritesvoice)
        await textchannel.send(
            "{member1} has been matched with {member2}".format(member1=member1.mention, member2=member2.mention))
        embed = discord.Embed(title="You have been matched!",
                              description="Be nice, don't advertise, report pedos/horny e-boys to the janitor. Type >help for more options",
                              color=0xff42f2)
        embed.add_field(name="How do I leave a chatroom?",
                        value="type >leave inside the chatroom",
                        inline=False)
        embed.add_field(name="Can I match up with multiple people at once?",
                        value="No, you cannot, you must type >leave inside the chatroom/textchannel, then type >matchme again in dms",
                        inline=False)
        await textchannel.send(embed=embed)
        await member1.remove_roles(discord.utils.get(guild.roles, name="Matching"))
        await member2.remove_roles(discord.utils.get(guild.roles, name="Matching"))
        await member1.add_roles(discord.utils.get(guild.roles, name="Matched"))
        await member2.add_roles(discord.utils.get(guild.roles, name="Matched"))
        await bot.get_channel(config["serverlogid"]).send("Match Made Between Users")
    else:
        await bot.get_channel(config["serverlogid"]).send("Match Cannot be Made")

@tasks.loop(seconds=240)
async def conversationstarter():
    channellist = []
    for discord.TextChannel in bot.get_guild(config["serverid"]).text_channels:
        if discord.TextChannel.name == "matched-with-user":
            channellist.append(discord.TextChannel)
    if not channellist:
        await bot.get_channel(config["serverlogid"]).send("Unable to create conversation")
    else:
        conversationchannel = random.choice(channellist)
        lines = open('settings/conversationstarters.txt').read().splitlines()
        myline = random.choice(lines)
        str(myline)
        await conversationchannel.send(myline)

@tasks.loop(seconds=5)
async def presencenummatched():
    memberlist = []
    guild = bot.get_guild(config["serverid"])
    for member in guild.members:
        if discord.utils.get(guild.roles, name="Matched") in member.roles:
            memberlist.append(member)
    await bot.change_presence(activity=discord.Game(name="with {memberlist} matched users!".format(memberlist=len(memberlist))))

bot.run(config["bottoken"], bot=True, reconnect=True)