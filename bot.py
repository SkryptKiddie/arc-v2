import discord, pushover, json
import os, sys, time, datetime
from tinydb import TinyDB, Query
from discord.ext import commands

# get the config data from config.json
with open('./config.json', 'r') as config_file:
    config = json.load(config_file)
bot_token = config["bot_token"]
bot_prefix = config["bot_prefix"]
bot_name = config["bot_name"]
bot_id = config["bot_id"]
owner_id = config["owner_id"]
# define the pushover integration vars for error logging
pushover.config.api_key = config["pushover_api_key"]
pushover.config.user_key = config["pushover_user_key"]
# setup the database for user data
userdata = TinyDB("db/users.db", indent=4)
serverdata = TinyDB("db/servers.db", indent=4)
search = Query()
# shortcuts
current_time = datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
current_datetime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
red = 0xff0000
green = 0x2eff51
# extensions
cogs = ["cogs.main", "cogs.mod", "cogs.owner"]

class checks: # contains the ownercheck and botcheck for command execution
    @staticmethod
    def ownercheck(ctx):
        if str(ctx.message.author.id) == str(config.owner_id):
            return True # is the owner
        else:
            return False # is not the owner
    
    @staticmethod
    def botcheck(ctx):
        if ctx.message.author.bot == True:
            return True # is a bot
        else:
            return False # is not a bot

checks = checks() # define the checks class
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(bot_prefix), 
    case_insensitive=True,
    description="Just another Discord bot in a sea of code.") # setup the discord

print("{} | Bot starting...".format(current_time))
@bot.event
async def on_ready():
    print("{} | Connected to Discord API!".format(current_time))
    await bot.change_presence(activity=discord.Game(name="{}help | Serving {} servers and {} users!".format(bot_prefix, len(bot.servers), len(set(bot.get_all_members()))),type=3))
    print("{} | Bot ready!".format(current_time))

#
# cog loading commands
#

@commands.check(checks.ownercheck)
@bot.command(pass_context=True)
async def load(ctx, cog_name : str):
    """Loads an unloaded cog."""
    try:
        bot.load_extension(cog_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("`{}` loaded successfully.".format(cog_name))

@commands.check(checks.ownercheck)
@bot.command(pass_context=True)
async def unload(ctx, cog_name : str):
    """Unloads a loaded cog."""
    bot.unload_extension(cog_name)
    await bot.say("`{}` unloaded successfully.".format(cog_name))

@commands.check(checks.ownercheck)
@bot.command(pass_context=True)
async def reload(ctx, cog_name : str):
    """Reloads a loaded cog."""
    try:
        bot.unload_extension(cog_name)
        bot.load_extension(cog_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("`{}` reloaded successfully.".format(cog_name))

#
# error handling
#

@bot.event # handle missing subcommand variables
async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            embed=discord.Embed(title="Missing subcommand values", description=page, color=red)
            await bot.send_message(ctx.message.channel, embed=embed)

#
# bot events
#

if __name__ == "__main__": # load all cogs at start
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print("Error while loading {}\n{}".format(cog, exc))
            pushover.main.sendMessage(dest=pushover.config.user_key, title="Initialisation error!", message="""Error while loading the {} cog\n{}""".format(cog, exc), priority="-1")

@bot.event
async def on_guid_join(server): 
    pushover.main.sendMessage(
        dest=pushover.config.user_key, 
        title="Joined a server!", 
        message="""Server name: {}\nServer ID: {}\nMember count: {}""".format(server.name, server.id, len(server.members)),
        priority="-1")
    serverdata.insert({"server_name": "{}".format(server.name), "server_id": "{}".format(server.id), "server_owner": "{}".format(server.owner), "joined": "{}".format(current_datetime)}) # add server to database
    await bot.change_presence(activity=discord.Game(name="{}help | Serving {} servers and {} users!".format(config.bot_prefix, len(bot.servers), len(set(bot.get_all_members()))),type=3)) 

@bot.event
async def on_guid_remove(server): 
    pushover.main.sendMessage(
        dest=pushover.config.user_key, 
        title="Removed from a server!", 
        message="""Server name: {}\nServer ID:""".format(server.name, server.id),
        priority="-1")
    serverdata.remove(search.server_id == server.id) # remove server from database
    await bot.change_presence(activity=discord.Game(name="{}help | Serving {} servers and {} users!".format(config.bot_prefix, len(bot.servers), len(set(bot.get_all_members()))),type=3)) 

bot.run(bot_token) # starts the bot
