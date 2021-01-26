import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Cog
import yaml

intents = discord.Intents.default()
intents.members = True

config = yaml.load(open("settings/settings.yaml"))

class onmemberjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def isandy(ctx):
        return ctx.author.id == config["ownerid"]

    @commands.command()
    @commands.check(isandy)
    async def understoodterms(self, ctx):
        embed = discord.Embed(title="What is this server and how does this all work?",
                              color=0xff42f2)
        y = await ctx.message.channel.send(embed=embed)
        await ctx.message.channel.send(">You can talk to people like Omegle on discord but without all of the spam and horny people.")
        await ctx.message.channel.send(">This is all run by a custom programmed bot to do all the matchmaking, and filtering.")
        await ctx.message.channel.send(">You can have nice, comfy, and private, conversations now.")
        await ctx.message.channel.send(">Get matched into one role, one text-channel, one voice-channel, with no issues.")
        await ctx.message.channel.send(">This is a server run with no moderation, moderation will be by you, the user, and for you.")
        await ctx.message.channel.send(">This is a place where you will most importantly create friendships and enjoy yourself.")
        embed2 = discord.Embed(title="So are you ready to make new friends?",
                               description="and are you ready to see discord in a whole new twist?",
                               color=0xff42f2)
        embed2.add_field(name="When you're ready...",
                        value="Upvote the thumbs up emoji to join in right now!",
                        inline=False)
        embed2.set_image(url=config["serverlogo"])
        x = await ctx.message.channel.send(embed=embed2)
        await x.add_reaction('\N{THUMBS UP SIGN}')

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(config["serverid"])
        if payload.message_id == config["payloadmessageid"]:
            role = discord.utils.get(guild.roles, name="Member")
            member = discord.utils.get(guild.members, id=payload.user_id)
            await member.add_roles(role)

def setup(bot):
    bot.add_cog(onmemberjoin(bot))