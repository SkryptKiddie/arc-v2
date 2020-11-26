import discord, asyncio, aiohttp, json # mod cog for Arc
import json, os, sys, datetime
from discord.ext import commands
from tinydb import TinyDB, Query
#shortcuts
current_time = datetime.datetime.now().time()
red = 0xff0000
green = 0x2eff51
# load the config.json
with open('./config.json', 'r') as config_file:
    config = json.load(config_file)
# load the userdata database
serverdata = TinyDB("db/servers.db", indent=4)
userdata = TinyDB("./db/users.db", indent=4)
search = Query()

class checks: # contains the ownercheck and botcheck for command execution
    @staticmethod
    def ownercheck(ctx):
        if ctx.message.author.id == str(config["owner_id"]):
            return True # is the owner
        else:
            return False # is not the owner

    @staticmethod
    def botcheck(ctx):
        if ctx.message.author.bot == True:
            return False # is a bot
        else:
            return True # is not a bot

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, member: discord.Member, *, reason):
        """Kick a specified user."""
        if self.message.author.server_permissions.administrator or self.message.author.server_permissions.kick_members:
            try:
                await self.bot.kick(member) # kick the user
                embed=discord.Embed(title="Kicked", description="{} was kicked by {} for {}".format(self.message.author, self.member.name, reason), color=green)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
            except:
                embed=discord.Embed(title="Error!", description="Unable to kick user.", color=red)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
        else:
            embed=discord.Embed(title="Unauthorised.", description="You do not have permission to kick.", color=red)
            embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
            await self.send(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, member: discord.Member, *, reason):
        """Ban a specified user."""
        if self.message.author.server_permissions.administrator or self.message.author.server_permissions.ban_members:
            try:
                await self.bot.ban(member) # ban the user
                embed=discord.Embed(title="Banned", description="{} was banned by {} for {}".format(self.message.author, self.member.name, reason), color=green)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
            except:
                embed=discord.Embed(title="Error!", description="Unable to ban user.", color=red)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
        else:
            embed=discord.Embed(title="Unauthorised.", description="You do not have permission to ban.", color=red)
            embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
            await self.send(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, user: discord.Member, *, nickname):
        """Changes the nickname of a specified user."""
        if self.message.author.server_permissions.administrator or self.message.author.server_permissions.manage_nicknames:
            try:
                await self.bot.change_nickname(user, nickname)
                embed = discord.Embed(title="User nicknamed!", description="**{}**'s nickname was successfully changed to **{}**!".format(user, nickname), color=green)
                embed.set_author(name=self.message.author, icon_url=self.message.author.avatar_url)
                embed.set_footer(text="Responsible moderator - " + str(self.message.author))
                await self.bot.say(embed=embed)
            except:
                embed=discord.Embed(title="Error!", description="Unable to change nickname of user.", color=red)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
        else:
            embed = discord.Embed(title="Unauthorised.", description="You do not have permission to change nicknames.", color=red)
            await self.bot.say(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, amount):
        """Purge an amount of messages."""
        if self.message.author.server_permissions.administrator or self.message.author.server_permissions.manage_messages:
            try:
                await self.bot.purge_from(self.message.channel, limit=int("1"))
                await self.bot.purge_from(self.message.channel, limit=int(amount))
                embed=discord.Embed(title="Purged successfully!", description="Purged " + amount + " message(s).", color=green)
                embed.set_footer(text="Responsible moderator - " + str(self.message.author))
                await self.bot.say(embed=embed)
            except:
                embed=discord.Embed(title="Error!", description="Unable to change nickname of user.", color=red)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
        else:
            embed = discord.Embed(title="Unauthorised.", description="You do not have permission to change nicknames.", color=red)
            await self.bot.say(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, member: discord.Member, *, role):
        """Add a role to a user (case sensitive)"""
        if self.message.author.server_permissions.administrator or self.message.author.server_permissions.manage_roles:
            try:
                role = discord.utils.get(member.server.roles, name=role)
                await self.bot.add_roles(member, role)
                embed = discord.Embed(title="Role added", description="Role was added!".format(self.message.author, role, member), color=green)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.bot.say(embed=embed)
            except:
                embed=discord.Embed(title="Error!", description="Unable to change nickname of user.", color=red)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
        else:
            embed = discord.Embed(title="Unauthorised.", description="You do not have permission to change nicknames.", color=red)
            await self.bot.say(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, member: discord.Member, *, role):
        """Remove a role (case sensitive)"""
        if self.message.author.server_permissions.administrator or self.message.author.server_permissions.manage_roles:
            try:
                role = discord.utils.get(member.server.roles, name=role)
                await self.bot.remove_roles(member, role)
                embed = discord.Embed(title="Role removed", description="Role was removed!".format(self.message.author, role, member), color=0x176cd5)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.bot.say(embed=embed)
            except:
                embed=discord.Embed(title="Error!", description="Unable to change nickname of user.", color=red)
                embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
                await self.send(embed=embed)
        else:
            embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0x176cd5)
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))