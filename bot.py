import aiohttp
import random
import json
import os
import datetime
import sys
import asyncio
import re
import datetime
from subprocess import check_output
try:
    import requests
except:
    print("You don't have requests installed, installing it now...")
    check_output("pip3 install requests", shell=True)
    try:
        import requests
        print("Requests successfully installed.")
    except:
        sys.exit("Requests didn't successfully install, exiting...")
from time import *
try:
	import discord
except:
    print("You don't have discord.py installed, installing it now...")
    try:
        check_output("pip3 install discord.py", shell=True)
        import discord
        print("Discord.py successfully installed.")
    except:
        sys.exit("Discord.py didn't successfully install, exiting...")
try:
    from pyfiglet import figlet_format
except:
    print("You don't have pyfiglet installed, installing it now...")
    try:
        check_output("pip3 install pyfiglet", shell=True)
        import pyfiglet
        print("Pyfiglet successfully installed.")
    except:
        sys.exit("Pyfiglet didn't successfully install, exiting...")

def setup(settings):
    print("First time setup, prepare your anus for some questions.")
    token = input("What's your Discord token? (To see how to get it go to https://github.com/PlanetTeamSpeakk/DiscordSelfBot#token)\n")
    if token.startswith("\""):
        token = token[1:]
    if token.endswith("\""):
        token = token[:(len(token) - 1)]
    prefix = input("What should your prefix be?\n")
    invite = input("What's the permanent invite link for you Discord server? Type None if you don't have one.\n")
    settings['token'] = token
    settings['prefix'] = prefix
    settings['invite'] = invite
    bot = commands.Bot(command_prefix=prefix, description=description, self_bot=True)
    settings_file = None
    with open("data/dsb/settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4, sort_keys=True, separators=(',', ' : '))
    print("You're all set! Bot is starting, don't mind the unclosed client session part, just wait a bit.")
        
cmds = {'No Category': {'help': {'help': 'Shows this screen.', 'usage': 'help [command]'}}}
        
description = "A Discord SelfBot written by PlanetTeamSpeak#4157."
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/dsb"):
    os.makedirs("data/dsb")
if not os.path.exists("data/dsb/settings.json"):
    with open("data/dsb/settings.json", "w") as settings:
        json.dump({'token': 'token_here', 'whitelist': ['your_id'], 'prefix': 'prefix_here', 'invite': 'invite_here'}, settings, indent=4, sort_keys=True, separators=(',', ' : '))
        settings = None
from discord.ext import commands
with open("data/dsb/settings.json", "r") as settings_file:
    settings = json.load(settings_file)
    if 'token' not in settings.keys():
        setup(settings)
    token = settings['token']
    whitelist = settings['whitelist']
    prefix = settings['prefix']
    invite = settings['invite']
    bot = commands.Bot(command_prefix=prefix, description=description, self_bot=True)
    settings_file = None
    asked = False
    for key in settings:
        if "_here" in settings[key]:
            setup(settings)
            break

started = datetime.datetime.utcnow()
dry_run = False
    
version = "1.3.3"
print("Checking for updates...")
new_version = requests.get("https://raw.githubusercontent.com/PlanetTeamSpeakk/DiscordSelfBot/master/version.json").json()[0]
if new_version != version:
    sys.exit("An update was detected, please update the bot by running update.bat. (Your version: {}, newest version: {})".format(version, new_version))
if dry_run:
    sys.exit("Dry run, no updates found exiting...")
else:
    print("No updates found, logging in...")

@bot.event
async def on_ready():
    login_time = datetime.datetime.utcnow() - started
    print("\nLogin succesfull, took {}ms, started on {}.".format(login_time.seconds + login_time.microseconds/1E6, started.strftime("%d %b %Y %X")))
    print("DiscordSelfBot written by PlanetTeamSpeak#4157.\n")
    if "your_id" in whitelist:
        id = bot.user.id
        settings['whitelist'].remove("your_id")
        settings['whitelist'].append(id)
        save_settings()
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("extensions"):
        os.makedirs("extensions")
    print("--------")
    print("Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("--------")
    print("Prefix: " + prefix)
    print()
    
@bot.event
async def on_message(message):
    msgchan = message.channel                    
    if await command(message, "help", True):
        cmd = message.content[len(prefix + "help "):]
        help_cmds = ""
        if cmd == "":
            for ext in cmds.keys():
                help_cmds += "\n**{}**:\n".format(ext)
                for cmda in cmds[ext].keys():
                    if len(cmda + cmds[ext][cmda]['help']) > 70:
                        help_cmds += "\t- `{}`: {}...\n".format(cmda, cmds[ext][cmda]['help'][:70])
                    else:
                        help_cmds += "\t- `{}`: {}\n".format(cmda, cmds[ext][cmda]['help'])
                    if len(help_cmds) > 1750:
                        await say(msgchan, help_cmds)
                        help_cmds = ""
            await say(msgchan, help_cmds)
            help_cmds = ""
            await say(msgchan, "To get information of a specific command type {}help <command>".format(prefix))
        else:
            error = 0
            for ext in cmds.keys():
                try:
                    temp = cmds[ext][cmd]['help']
                    await say(msgchan, "`{}` ({}):\n{}\n\nUsage:\n`{}`".format(cmd, ext, cmds[ext][cmd]['help'], prefix + cmds[ext][cmd]['usage']))
                    temp = None
                except:
                    temp = None
                    error += 1
            if error == len(cmds.keys()):
                await say(msgchan, "The command you entered ({}) could not be found.".format(cmd))
                
async def command(message, cmd, del_msg):
    if message.content.lower().startswith(prefix.lower() + cmd):
        if message.author.id in whitelist:
            if del_msg:
                try:
                    await bot.delete_message(message)
                except:
                    pass
            if cmd.endswith(" "):
                print("{} just used the {}command in {} ({}).".format(message.author, cmd, message.server, message.channel))
            else:
                print("{} just used the {} command in {} ({}).".format(message.author, cmd, message.server, message.channel))
            return True
        else:
            return False
    else:
        return False
        
def save_settings():
    with open("data/dsb/settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4, sort_keys=True, separators=(',', ' : '))
    reload_settings()
    
def reload_settings():
    settings = None
    with open("data/dsb/settings.json", "r") as settings_file:
        settings = None
        settings = json.load(settings_file)
        email = settings['token']
        prefix = settings['prefix']
        whitelist = settings['whitelist']
        invite = settings['invite']
        settings_file = None
        
async def say(channel, message=None, embed=None):
    if embed is not None:
        await bot.send_message(channel, embed=embed)
    else:
        await bot.send_message(channel, message)

def is_owner(member):
    if int(member.id) == int(bot.user.id):
        return True
    else:
        return False
        
try:
    bot.load_extension("extensions.owner")
except Exception as e:
    print("Failed to load owner:\n{}".format(e))
asyncio.sleep(0.1)
with open("data/dsb/extensions.json", "r") as extensions:
    extensions = json.load(extensions)
        
for extension in extensions:
    if extensions[extension]:
        try:
            bot.load_extension("extensions." + extension)
        except Exception as e:
            print("Failed to load {}:\n{}".format(extension, e))
e = None
try:
    bot.run(token, bot=False)
except Exception as e:
    while e != None:
        print("An improper token has been passed, please insert a proper one.")
        token = input("> ")
        try:
            bot.run(token, bot=False)
            settings['token'] = token
            save_settings()
            e = None
        except Exception as e:
            pass
    