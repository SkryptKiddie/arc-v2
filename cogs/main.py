import discord, asyncio, aiohttp # main cog for Arc
import json, os, sys, datetime, psutil, time
from discord.ext import commands
from tinydb import TinyDB, Query
#shortcuts
current_time = datetime.datetime.now().time()
start_time = time.time()
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

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    async def ping(self):
        """Test the bot's response time."""
        ptime = time.time()
        embed = discord.Embed(Title='Pong!', color=green)
        embed.add_field(name="Pong!", value="Calculating...")
        embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
        ping3 = await self.bot.send(embed=embed)
        ping2 = time.time() - ptime
        ping1 = discord.Embed(Title='Pong!', color=green)
        ping1.add_field(name='Pong!', value='{} ms.'.format(int((round(ping2 * 1000)))))
        ping1.embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
        await ping3.edit(embed=ping1)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    async def test(self):
        """Test command."""
        embed=discord.Embed(title="Test", description="Test command", color=green)
        embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
        await self.bot.say(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    async def stats(self):
        """Current bot statistics."""
        embed=discord.Embed(title="Bot statistics", color=green)
        embed.add_field(name="Server count", value=(len(self.bot.servers)), inline=True)
        embed.add_field(name="Member count", value=(len(set(self.bot.get_all_members()))), inline=True)
        embed.add_field(name="Database entries", value=(len(userdata.all())), inline=True)
        embed.add_field(name="CPU usage", value=(psutil.cpu_percent()), inline=True)
        embed.add_field(name="RAM usage", value=(psutil.virtual_memory()), inline=True)
        embed.add_field(name="Uptime", value=(time.time() - start_time), inline=True)
        embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
        await self.bot.say(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    async def userinfo(self, user: discord.Member=None):
        """Displays user information."""
        if not user: # if no user is specified, we'll assume the command issuer
            embed = discord.Embed(title="Your info.", color=green)
            embed.add_field(name="Username", value=self.message.author.name + "#" + self.message.author.discriminator, inline=True)
            embed.add_field(name="ID", value=self.message.author.id, inline=True)
            embed.add_field(name="Status", value=self.message.author.status, inline=True)
            embed.add_field(name="Roles", value=len(self.message.author.roles))
            embed.add_field(name="Joined", value=self.message.author.joined_at)
            embed.add_field(name="Created", value=self.message.author.created_at)
            embed.add_field(name="Bot?", value=self.message.author.bot)
            embed.set_thumbnail(url=self.message.author.avatar_url)
            embed.set_author(name=self.message.author, icon_url=self.message.author.avatar_url)
            await self.bot.say(embed=embed)
        else: # otherwise, get details of arg'd user
            embed = discord.Embed(title="{}'s info".format(user), color=green)
            embed.add_field(name="Username", value=user.name + "#" + user.discriminator, inline=True)
            embed.add_field(name="ID", value=user.id, inline=True)
            embed.add_field(name="Status", value=user.status, inline=True)
            embed.add_field(name="Roles", value=len(user.roles))
            embed.add_field(name="Joined", value=user.joined_at)
            embed.add_field(name="Created", value=user.created_at)
            embed.add_field(name="Bot?", value=user.bot)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_author(name=self.message.author, icon_url=self.message.author.avatar_url)
            await self.bot.say(embed=embed)

    @commands.check(checks.botcheck)
    @commands.command(pass_context=True)
    async def avatar(self, user: discord.Member=None):
        """Displays users avatar."""
        if not user:
            embed = discord.Embed(color=green)
            embed = discord.Embed(title="View full image.", url=self.message.author.avatar_url, color=0x176cd5)
            embed.set_image(url=self.message.author.avatar_url)
            embed.set_author(name=self.message.author, icon_url=self.message.author.avatar_url)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(color=green)
            embed = discord.Embed(title="View full image.", url=user.avatar_url, color=0x176cd5)
            embed.set_image(url=user.avatar_url)
            embed.set_author(name=self.message.author, icon_url=self.message.author.avatar_url)
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Main(bot))