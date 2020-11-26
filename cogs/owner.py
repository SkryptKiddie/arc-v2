import discord, asyncio, aiohttp, json # owner cog for Arc
import subprocess, datetime, pushover, sys, os
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

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(checks.ownercheck)
    @commands.command(pass_context=True)
    async def poweroff(self):
        """Shutdown the bot."""
        embed=discord.Embed(title="Stopping bot...", color=green)
        embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
        await self.bot.say(embed=embed)
        pushover.main.sendMessage(dest=pushover.config.user_key, title="bot stopped", message="bot was shutdown by {}".format(self.message.author), priority="-1")
        print("{} | Shutdown command issued.".format(current_time))
        await self.bot.logout() # logout from the discord API
        sys.exit() # terminate the process

    @commands.check(checks.ownercheck)
    @commands.command(pass_context=True)
    async def reboot(self):
        """Restart the bot."""
        embed=discord.Embed(title="Restarting bot...", color=green)
        embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
        await self.bot.say(embed=embed)
        pushover.main.sendMessage(dest=pushover.config.user_key, title="bot restarted", message="bot was restarted by {}".format(self.message.author), priority="-1")
        print("{} | Restart command issued.".format(current_time))
        await self.bot.logout() # logout from the discord API
        subprocess.call([sys.executable, "bot.py"]) # restarts the bot process

    @commands.check(checks.ownercheck)
    @commands.command(pass_context=True)
    async def leaveserver(self, id):
        """Force leave a server."""
        try:
            toleave = self.bot.get_server(id)
            await self.bot.leave_server(toleave)
            embed=discord.Embed(title="Left server successfully!", color=green)
            embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
            await self.bot.say(embed=embed)
            await self.bot.change_presence(activity=discord.Game(name="{}help | Serving {} servers and {} users!".format(config.bot_prefix, len(self.servers), len(set(self.get_all_members()))),type=3))
        except:
            embed=discord.Embed(title="Error!", description="Unable to leave server.", color=red)
            embed.set_author(name="Requested by {}".format(str(self.message.author)), icon_url=self.message.author.avatar_url)
            await self.send(embed=embed)


    @commands.check(checks.ownercheck)
    @commands.command(pass_context=True)
    async def say(self, *, message):
        """Send a message through the bot."""
        await self.bot.say(message)

    @commands.check(checks.ownercheck)
    @commands.command(pass_context=True)
    async def _eval(self, *, code):
        """Evaluate code and return the output."""
        global_vars = globals().copy()
        global_vars['bot'] = self.bot
        global_vars['message'] = self.message
        global_vars['author'] = self.message.author
        global_vars['channel'] = self.message.channel
        global_vars['server'] = self.message.server

        try:
            result = eval(code, global_vars, locals())
            if asyncio.iscoroutine(result):
                result = await result
            result = str(result) # the eval output was modified by me but originally submitted by DJ electro
            embed=discord.Embed(title="Evaluated successfully.", color=green)
            embed.add_field(name="Input", value="```" + code + "```")
            embed.add_field(name="Output", value="```" + result + "```")
            await self.bot.say(embed=embed)
        except Exception as error:
            embed=discord.Embed(title="Evaluated with problems.", color=red)
            embed.add_field(name="Input", value="```" + code + "```", inline=True)
            embed.add_field(name="Output", value='```{}: {}```'.format(type(error).__name__, str(error)))
            await self.bot.say(embed=embed)
            return

def setup(bot):
    bot.add_cog(Owner(bot))