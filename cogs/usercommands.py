import discord
from discord.ext import commands
import random
import yaml

intents = discord.Intents.default()
intents.members = True

config = yaml.load(open("settings/settings.yaml"))

class usercommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def isandy(ctx):
        return ctx.author.id == config["ownerid"]

    @commands.command(name='matchme', no_pm=False)
    async def match_me(self, ctx):
        guild = self.bot.get_guild(config["serverid"])
        userroles = guild.get_member(ctx.message.author.id).roles
        if discord.utils.get(guild.roles, name="Member") in userroles:
            guild = self.bot.get_guild(config["serverid"])
            userroles = guild.get_member(ctx.message.author.id).roles
            if discord.utils.get(guild.roles, name="Matching") in userroles:
                await ctx.message.author.send(
                    "You are already in queue to match with a user! Type >leavequeue to leave the queue.")
            elif discord.utils.get(guild.roles, name="Matched") in userroles:
                await ctx.message.author.send("You are already matched up with a user!")
            else:
                await ctx.message.author.send("You are now in queue to match with a user")
                await guild.get_member(ctx.message.author.id).add_roles(discord.utils.get(guild.roles, name="Matching"))
        else:
            await ctx.message.author.send("You are not a member! Make sure you emoted to verify!")


    @commands.command(name='leavequeue', no_pm=False)
    async def leave_queue(self, ctx):
        guild = self.bot.get_guild(config["serverid"])
        userroles = guild.get_member(ctx.message.author.id).roles
        if discord.utils.get(guild.roles, name="Matched") in userroles:
            await ctx.message.author.send("You are already matched up with a user!")
        if discord.utils.get(guild.roles, name="Matching") in userroles:
            await ctx.message.author.send("You have left the queue to match up with a user.")
            await guild.get_member(ctx.message.author.id).remove_roles(discord.utils.get(guild.roles, name="Matching"))
        else:
            await ctx.message.author.send("You are not in queue.")

    @commands.command(name='leave', no_pm=True)
    async def leave(self, ctx):
        if ctx.message.channel.id != 797175948247695372:
            memberlist = []
            for member in ctx.message.channel.members:
                memberlist.append(member)
            await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name="Matched"))
            memberlist2 = []
            await ctx.message.channel.set_permissions(ctx.message.author, read_messages=False, send_messages=False)
            for member in ctx.message.channel.members:
                memberlist2.append(member)
            await ctx.message.channel.send("{member} User has left".format(member=ctx.message.author.id))
            if len(memberlist2) <= 2:
                await ctx.message.channel.delete()
            vcmemberlist = []
            for discord.VoiceChannel in self.bot.get_guild(config["serverid"]).voice_channels:
                if discord.VoiceChannel.permissions_for(ctx.message.author).view_channel and discord.VoiceChannel.permissions_for(ctx.message.author).connect:
                    await discord.VoiceChannel.set_permissions(ctx.message.author, connect=False, view_channel=False)
                    for member in ctx.message.channel.members:
                        vcmemberlist.append(member)
                    if len(vcmemberlist) <= 2:
                        await discord.VoiceChannel.delete()
        else:
            await ctx.message.channel.send("Don't leave...")


    @commands.command(name='checkqueue', no_pm=False)
    async def checkqueue(self, ctx):
        memberlist = []
        guild = self.bot.get_guild(config["serverid"])
        for member in guild.members:
            if discord.utils.get(guild.roles, name="Matching") in member.roles:
                memberlist.append(member)
        await ctx.message.author.send("There are currently {memberlist} in queue!".format(memberlist=len(memberlist)))

    @commands.command(name='cleanup')
    @commands.check(isandy)
    async def cleanup(self, ctx):
        guild = self.bot.get_guild(config["serverid"])
        for member in guild.members:
            if discord.utils.get(guild.roles, name="Matched") in member.roles:
                await member.remove_roles(discord.utils.get(guild.roles, name="Matched"))
                await ctx.message.author.send("{memberid} has been removed of Matched".format(memberid=member.id))
        for discord.TextChannel in self.bot.get_guild(config["serverid"]).text_channels:
            if discord.TextChannel.name == "matched-with-user":
                await discord.TextChannel.delete()
        for discord.VoiceChannel in self.bot.get_guild(config["serverid"]).voice_channels:
            if discord.VoiceChannel.name == "Matched With User":
                await discord.VoiceChannel.delete()
def setup(bot):
    bot.add_cog(usercommands(bot))