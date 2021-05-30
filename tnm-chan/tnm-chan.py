### TNM-chan ###
### v 21.149 ###

### BEGIN SYSTEM VARIABLES ###
# Set your command prefix here.
pre = 'tnm!'

# If you say "colour" instead of "color," change this variable to "True", and I'll change everything accordingly.
useColour = False

# Type your Discord username in quotes, then add your user ID - make sure these are right, because I use both on occasion!
sysop = ''
soID = int()

# Before launching the bot, take note of any moderators that have access to all rooms, and copy their IDs into this list (separated by commas). 
opIDs = [

]
# Type your open room names into this list (separated by commas), with each entry surrounded by quotes.
openRooms = [
'lobby'
]

# Choose whether or not you'll use debug commands. If you are, type your debug room's name here.
useDebug = True # Make sure this is a boolean ("True" or "False")!
debugSet = 'bot-debug'

# This is your server's color library.
colorset = {
    hex(0x000000): 'tooblack', # Don't touch this one! If the color is pure black, Discord will just replace it with no color, which we don't want.

# Set some default color values here. Here are the ones in the official server.
    hex(0xff0000): 'red',
    hex(0xe67e22): 'orange',
    hex(0xffff00): 'yellow',
    hex(0x00ff00): 'green',
    hex(0x00ffff): 'teal',
    hex(0x0080ff): 'blue',
    hex(0x0000ff): 'indigo',
    hex(0x9b59b6): 'purple',
    hex(0xff00ff): 'magenta',
    hex(0xff98ff): 'pink',
    hex(0xffffff): 'white',
    hex(0x010101): 'black',
}

### END SYSTEM VARIABLES ###
## I'm getting started!

# First, I'll import/load libraries.
import traceback
import os
import shelve
import asyncio
from random import choice

### THESE MODULES MUST BE INSTALLED WITH PIP! ###
import termcolor
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Due to a Discord...thing, I need to set intents now. Thanks, Discord.
intents = discord.Intents.all()

# Next, I'll define some subroutines.
def getKey(vin): # This is for finding a specific value in a color library.
    for key, value in colorset.items(): 
         if vin == value: 
             return key 

    raise KeyError()

# Now, the token specified in the .env is used to get in to Discord's APIs.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
serverName = os.getenv('DISCORD_GUILD')

# I'm setting my command prefix.
bot = commands.Bot(command_prefix=str(pre), intents=intents)

# I'll remove the default "help" command so I can use my own.
bot.remove_command('help')

# Here's some information regarding termcolor.
def Information(skk): print("\033[97m {}\033[00m" .format(skk)) # Gray

def Success(skk): print("\033[92m {}\033[00m" .format(skk)) # Green

def UserErr(skk): print("\033[93m {}\033[00m" .format(skk)) # Yellow
def SysErr(skk): print("\033[91m {}\033[00m" .format(skk)) # Red

def Permission(skk): print("\033[95m {}\033[00m" .format(skk)) # Purple
def Intent(skk): print("\033[34m {}\033[00m" .format(skk)) # Blue
def Conversion(skk): print("\033[96m {}\033[00m" .format(skk)) # Cyan

# Now, I'll set up constant variables here, as well as define a couple more subroutines.
firstConnect = True

overwrite = discord.PermissionOverwrite()
overwrite.send_messages=True
overwrite.read_messages=True

if useColour:
    clr = 'colour'
else:
    clr = 'color'

dmWelcome = '> **Hi there, and welcome to ' + str(serverName) + '!**\nI\'m TNM-chan, your android assistant. You might not know what to do at first, but don\'t worry! Type `tnm!help`, and I\'ll explain everything~\n\nBy the way, I ever go offline, let the operator know. Here\'s their username:\n```' + str(sysop) + '```\nThank you so much for joining! Enjoy your stay~'

# Here's how I set my status!~
async def setStatus(type=''):
    if type == "busy":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='with variables'), status=discord.Status.do_not_disturb)
    elif type == "color":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='with paint'), status=discord.Status.idle)
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for "tnm!help"'), status=discord.Status.online)

async def sendDebug(contents):
    if useDebug:
        await debug.send(contents)
    else:
        pass

# Now I'm ready, so I'll let you know!
Success('I\'m ready to go!')

# If all went well, I'll send a message to the terminal!
@bot.event
async def on_ready():
    global firstConnect
    global opMention
    global debug
    debug = 0 # This is only here so Rare doesn't have a panic attack... 
    if firstConnect:
        firstConnect = False
        # Setting up sysop mentions.
        opMention = await bot.fetch_user(int(soID))
        # Locating the debug room.
        de = [a for a in bot.get_all_channels() if a.name == debugSet]
        debug = de[0]
        await sendDebug(':green_circle: Connected.')
        Conversion('I\'ve connected to the server!\n')
    else:
        Conversion('I got disconnected, but I\'m back online!\n')
        await sendDebug(':blue_circle: Reconnected.')
    await setStatus()
# Here's how I welcome new users, and add them to #lobby-f1!
@bot.event
async def on_member_join(ctx):
    member = ctx
    Intent('Hey! ' + str(ctx) + ' just joined the server.')
    await sendDebug(':new: ' + str(ctx) + ' just joined the server.')
    await setStatus("busy")
    room = [a for a in bot.get_all_channels() if a.name == 'lobby-f1']
    await room[0].set_permissions(member, overwrite=overwrite)
    Information('They now have access to #lobby-f1...')
    await sendDebug('Access to #lobby-f1 given.')
    try:
        await member.send(dmWelcome)
        Information('and the welcome DM\'s been sent.')
        await sendDebug('Welcome DM was sent.')
    except discord.Forbidden:
        dmErrorFirst = 'Hi there, ' + str(ctx.mention) + '! To get the most out of the server, you\'ll need to turn on DMs from server members - at least, from *this* server. Otherwise, you won\'t be able to host rooms or see important information. I promise, we won\'t spam you!'
        await room[0].send(dmErrorFirst)
        UserErr('and I\'ve asked them to enable DMs from server members. Try to make sure they actually do this... ')
    Success('All set!\n')
    await setStatus()
    await sendDebug('--')
    
### Okay, here's my commands!

## This command send the user a message explaining each command.
@bot.command(name='help')
async def help(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!help')
    if ctx.guild:
        await ctx.message.delete()
    await ctx.message.author.send('> **COMMAND HELP**\n\n__Basic Commands:__\n```tnm!' + str(clr) + ' [input]: Set a custom role ' + str(clr) + '.\ntnm!goto floor|room [floor number]|[room name]: Move between rooms.\ntnm!help: Receive this screen in DMs.```\n__Host Commands:__\n```tnm!clear: Deletes, then recreates a room. All members inside will be added back to the room during recreation.\ntnm!close: Closes a room. This will send all users in the room back to that floor\'s lobby.\ntnm!lock: Locks a room. This prevents all users outside the room from entry.\ntnm!unlock: Unlocks a room. This will allow users to request permission to enter the room.```\n__Information Commands:__```tnm!license: View the Boost Software License v1.0 - the license that the TNM-chan source code is protected by.\ntnm!source: View the source code for TNM-chan.```')

## This command will allow a user to move between specific categories and channels, called "floors" and "rooms" respectively.
@bot.command(name='goto')
async def goto(ctx, arg1 = '[none]', arg2 = '[none]'):
    Information(str(ctx.message.author) + ' just ran: ' + str(pre) + 'goto ' + str(arg1) + ' ' + str(arg2) + '\n')
    await sendDebug(':arrow_forward: ' + str(ctx.message.author) + ' ran command "goto" with arg1 = `' + str(arg1) + '` and arg2 = `' + str(arg2) + '`.')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            UserErr(str(ctx.message.author) + ' tried to move, but sent the command in DMs and not in the server.\n')
            await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused!')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
# Defining consistent variables here.
        name = ctx.message.author
        source = ctx.message.channel
        src = str(source)
        dmError = 'Hi, ' + str(name.mention) + '! I tried to send you a DM, but it seems you\'ve disabled the option to allow DMs from server members. You\'ll need to turn that on to host rooms and receive important information from the server.'

## For floor movement...
        if arg1 == 'floor':
# First, I'll make sure the user didn't forget arg2, and send a DM if they did.
            if arg2 == '[none]':
                await sendDebug(':grey_exclamation: No arg2 provided. Command halted.\n--')
                try:
                    UserErr(str(name) + ' tried to move, but didn\'t say which floor to move to.\n')
                    await name.send('**Umm...** You need to tell me *which* floor you want to move to.')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Then, I'll let the terminal know I'm starting.
            destination = arg2.lower()
            Intent('I\'m starting floor movement... ')
            await sendDebug('Starting...')
# Next, I'll check to make sure the user is in that floor's lobby.
            sch = str(src.split('-')[0])
            lobby = 'lobby'
# If they aren't in the lobby...
            if sch != lobby:
# ...I'll send an error in a DM.
                await sendDebug(':grey_exclamation: The user isn\'t in the lobby. Command halted.\n--')
                try:
                    UserErr('They weren\'t in the lobby.\n')
                    await name.send('**Sorry, but...** You can\'t move floors outside of the lobby.\nTry running `tnm!goto room lobby` first.')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Otherwise...
# Next, I'll make sure the floor they request has a lobby.
            room = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())]
# If the lobby doesn't exist...
            if not room:
# ...I'll send an error in a DM.
                await sendDebug(':grey_exclamation: The floor provided had no lobby. Command halted.\n--')
                try:
                    UserErr('There was no lobby for floor ' + str(arg2.lower()) + '.\n')
                    await name.send('**Sorry, but...** The floor you requested doesn\'t have a lobby.')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Otherwise...
# Finally, I'll check to make sure I'm not wasting time.
# If it turns out I am...
            if source == room[0]:
# ...I'll send an error in a DM.
                await sendDebug(':grey_exclamation: User is already on the floor. Command halted.\n--')
                try:
                    UserErr('They tried to move to the same floor.\n')
                    await name.send('Looks like you\'re already there!')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source floor's #lobby.
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
            await sendDebug('Source perms removed.')
# Then, I'll send a message in the source room, stating the user has left.
            response = str(name.mention) + ' has left the room.'
            await source.send(response)
# Next, I'll send a message to the destination room, stating the user has joined.
            response = str(name.mention) + ' has entered the room.'
            target = 'lobby-f' + str(arg2.lower())
            destination = [a for a in bot.get_all_channels() if a.name == str(target)]
            await destination[0].send(response)
# Lastly, I'll give the user access to the destination floor's #lobby.
            await destination[0].set_permissions(name, overwrite=overwrite)
            Information('Given permissions for ' + str(destination[0]) + '...')
            await sendDebug('Target perms given.')
# And I'm finished!
            Success('Floor movement finished!\n')
            await sendDebug('Process complete!\n--')
            await setStatus()
            return

## For room movement...
        elif arg1 == 'room':
# I need to make sure the user didn't forget arg2, and send a DM if they did.
            if arg2 == '[none]':
                await sendDebug(':grey_exclamation: No arg2 was provided. Command halted.\n--')
                try:
                    UserErr(str(name) + ' tried to move, but didn\'t say which room to move to.\n')
                    await name.send('**Umm...** You need to tell me *which* room you want to move to. I can\'t really read minds...')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# I'll let the terminal know before starting.
            Intent('I\'m starting room movement... ')
            await sendDebug('Starting...')
# First, I'll see if arg2 is just a number (i.e., the command run was "tnm!goto room 3").
            try:
                newch = int(arg2)
# If it was, I'll append "room" to the beginning of arg2.
                convert = str('room' + arg2)
                Conversion('I just appended "room" to arg2.')
                await sendDebug('Appended "room" to arg2.')
# Otherwise...
            except ValueError:
# ...I can just leave it be.
                convert = str(arg2)
# Then, I'll make sure I'm not wasting time.
            destination = str(convert.lower()) + '-' + str(src.split('-')[1])
# If it turns out I am...
            if src == destination:
# ...I'll send an error message in a DM.
                await sendDebug(':grey_exclamation: Room movement unnecessary. Command halted.\n--')
                try:
                    UserErr('They tried to move to the same room.\n')
                    await name.send('Hey, I don\'t move you if you\'re already in the right room~')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Otherwise...
# Next, I'll make sure the room exists.
            newch = [a for a in bot.get_all_channels() if a.name == str(destination)]
# And if it doesn't...
            if not newch:
# ...I'll send an error in a DM.
                await sendDebug(':grey_exclamation: Room doesn\'t exist. Command halted.\n--')
                try:
                    UserErr('They tried to move to a room that doesn\'t exist.\n')
                    await name.send('**Sorry, but...** The room you requested doesn\'t exist.')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Otherwise...
# Next, I'll make sure the room isn't locked.
            if newch[0].topic == '🔒':
# If it is, I'll let them know.
                await sendDebug(':grey_exclamation: The room they tried to move to is locked. Command halted.\n--')
                try:
                    Information('The room is locked.')
                    await name.send('Unfortunately, the room is currently locked...')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Otherwise...
# Next, I'll check to see if I need to ask for permission to let them in.
            roomName = str(newch[0]).split('-')[0]
            if roomName not in openRooms:
# If I do, I'll see if anybody else is in the room.
                if len(newch[0].members) - len(opIDs) > 0:
# If there are people there, I'll ask for permission.
                    try:
                        try:
                            with shelve.open('chost') as f:
                                host = f[str(newch[0]) + '-host']
                        except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                            await sendDebug(':x: ' + str(opMention) + '**ERROR:** Room host was not found! Command halted.\n--')
                            SysErr('AHH!! I forgot the host of ' + str(newch[0]) + '!! Please fix this, like, soon!\n')
                            await name.send('**Eep!** Sorry, I forgot the host of `#' + str(newch[0]) + '`... Could you let `' + str(sysop) + '` know? He\'ll be able to fix it!')
                            await setStatus()
                            return
                        host = ctx.guild.get_member(host)
                        await sendDebug('Sending react message...')
                        reactm = await host.send(str(name) + ' wants to join ' + str(source) + '. You must react within 20 seconds to accept.')
                        await reactm.add_reaction('☑')
                        def check(reaction, user):
                            return reaction.count > 1 and reaction.message.id == reactm.id and str(reaction.emoji) == '☑'
                        Permission('I\'ve just asked for permission...')
                        await sendDebug('Sent. Waiting for reaction, or for twenty seconds to pass...')
                        await bot.wait_for('reaction_add', timeout=20, check=check)
                        await reactm.edit(content='Permission was granted.')
                        Success('Permission was granted by the host.')
                        await sendDebug('Permission granted. Continuing...')
                    except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
                        await sendDebug('Permission was automatically denied. Command halted.\n--')
                        try:
                            await reactm.edit(content='Permission was automatically denied.')
                            UserErr('No reaction from the host, so permission was automatically denied.\n')
                            await name.send('Unfortunately, the room host didn\'t let you in...')
                        except discord.Forbidden:
                            await source.send(dmError)
                        await setStatus()
                        return
                    except discord.Forbidden:
                        await source.send(dmError)
                    await setStatus()
                    return
# Or, if they're the first person to join that room...
                elif len(newch[0].members) - len(opIDs) == 0:
# ...I'll set them as that room's host, then let them know.
                    try:
# I'll check to see if chost.dat exists.
                        try:
                            with shelve.open('chost') as f:
                                pass
# If not...
                        except FileNotFoundError:
# ...I'll create it.
                            with open('chost', 'w') as f:
                                Information('I just created the chost file.')
                                await sendDebug('chost table was created.')
# After checking, I'll set the user as the host.
                        with shelve.open('chost') as f:
                            chost = {}
                            newid = int(name.id)
                            f[str(newch[0]) + '-host'] = int(newid)
                        await sendDebug(str(name) + ' was made the host.')
                        await name.send('**Hi!** Since you\'re the first person to join the room, you\'re its host. If anyone else tries to join, I\'ll ask you.')
                        Intent('I just made ' + str(name) + ' the room host.')
                    except discord.Forbidden:
                        await source.send(dmError)
                        await setStatus()
                        return
# If the user is currently the room host, and they're leaving...
            roomName = src.split('-')[0]
            if len(source.members) - 3 > 0 and (roomName not in openRooms):
                try:
                    with shelve.open('chost') as f:
                        hid = f[str(source) + '-host']
                except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                    await sendDebug(':x: ' + str(opMention) + '**ERROR:** Room host was not found! Command halted.\n--')
                    await name.send('**Eep!** Sorry, I think I forgot the host of `#' + str(source) + '`... Could you let `' + str(sysop) + '` know? He\'ll be able to fix it!')
                    SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this!\n')
                    await setStatus()
                    return
                host = ctx.guild.get_member(hid)
                if name == host:
# ...I'll assign another random member to be the new host of the room.
                    await sendDebug('The user currently leaving is the host. Assigning a new host...')
                    try:
                        newhost = choice(source.members)
                        nhid = int(newhost.id)
                        counter = 1
                        while nhid in opIDs: # This is so I don't accidentally make myself or admin the room host.
                            newhost = choice(source.members)
                            nhid = int(newhost.id)
                            counter = counter + 1
                            await sendDebug('User selected cannot be host. Trying again...')
                            print(nhid)
                        with shelve.open('chost') as f:
                            chost = {}
                            f[str(source) + '-host'] = int(nhid)
                        await sendDebug('Operation completed after ' + str(counter) + ' attempt(s).')
                        nhst = ctx.guild.get_member(newhost)
                        await sendDebug('New room host is ' + str(nhst) + '.')
                        await nhst.send('**Hi!** Since the previous host just left ' + str(source) + ', you\'re its new host now. If anyone else tries to join, I\'ll ask you.')
                        Intent(str(name) + ' just left, so I made ' + str(newhost) + 'the new room host. It took ' + str(counter) + ' attempt(s) to find a new host.')
                    except discord.Forbidden:
                        await source.send(dmError)
                        await setStatus()
                        return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source room.
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
            await sendDebug('Source perms taken.')
# Then, I'll send a message in the source room, stating the user has left.
            response = str(name.mention) + ' has left the room.'
            await source.send(response)
# Next, I'll send a message to the destination room, stating the user has joined.
            response = str(name.mention) + ' has entered the room.'
            await newch[0].send(response)
# Finally, I'll give the user access to the destination room.
            dsf = str(src.split('f')[1])
            await newch[0].set_permissions(name, overwrite=overwrite)
            Information('Given permissions for ' + str(convert) + '-f' + str(dsf[0]) + '...')
            await sendDebug('Target perms given.')
# And now I'm done!
            Success('Room movement finished!')
            await sendDebug('Process complete!')
# Oh, and if the current host is the last one to leave...
            if len(source.members) - 2 == 0 and (roomName not in openRooms):
# ...I'll recreate the room to clear out the messages.
                await sendDebug('Source is empty. Clearing channel...')
                Intent('Everyone\'s left, so I\'ll recreate the room to clear its messages...')
                pos = int(source.position)
                cch = await source.clone()
                await source.delete()
                await cch.edit(topic='', position=pos)
                Success('Alright, done!\n')
                await sendDebug('Done.\n--')
# Otherwise, I'll just add a new line to the terminal and stop.
            else:
                print('\n')
                await sendDebug('--')
            await setStatus()
            return

## In case they forgot arg1...
        elif arg1 == '[none]':
            await sendDebug(':grey_exclamation: No arg1 provided. Command halted.\n--')
            try:
                UserErr(str(name) + ' tried to move, but didn\'t provide an arg1.\n')
                await name.send('**Remember:** You need to type the following:\n```tnm!goto floor|room [floor number]|[room name]```')
            except discord.Forbidden:
                await source.send(dmError)
            await setStatus()
            return
# Or, if they mistyped arg1...
        else:
            await sendDebug(':grey_exclamation: Invalid arg1 provided. Command halted.\n--')
            try:
                UserErr(str(name) + ' tried to move, but provided an invalid arg1. They tried to use `' + str(arg1) + ' .\n')
                await name.send('**Sorry, but...** I can only understand `floor` or `room` for the first argument. You said `' + str(arg1) + '`.')
            except discord.Forbidden:
                await source.send(dmError)
            await setStatus()
            return

## This command will close a room, sending everyone back to the lobby and recreating the room.
@bot.command(name='close')
async def close(ctx):
    Information(str(ctx.message.author) + ' just ran: ' + str(pre) + 'close\n')
    await sendDebug(str(ctx.message.author) + ' ran command "clear".')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            UserErr(str(ctx.message.author) + ' tried to close the room, but sent the command in DMs and not in the server.\n')
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused....')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
        source = ctx.message.channel
        name = ctx.message.author
        dmError = 'Hi, ' + str(name.mention) + '! I tried to send you a DM, but it seems you\'ve disabled the option to allow DMs from server members. You\'ll need to turn that on to host rooms and receive important information from the server.'
# First, I'll check to make sure the room isn't an open room. If so...
        roomName = str(ctx.message.channel).split('-')[0]
        if (roomName in openRooms):
            UserErr('This is an open room...\n')
            await setStatus()
            return # ...I'll just stop there and not even bother telling them.
# Otherwise...
# I'll make sure the host wants to close the room...
        try:
            try:
                with shelve.open('chost') as f:
                    host = f[str(ctx.message.channel) + '-host']
            except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                await sendDebug(':x: ' + str(opMention) + '**ERROR:** Room host was not found! Command halted.\n--')
                await name.send('**Eep!** Sorry, I forgot the host of `#' + str(ctx.message.channel) + '`... Could you let `' + str(sysop) + '` know? He\'ll be able to fix it!')
                SysErr('AHH!! I forgot the host of ' + str(ctx.message.channel) + '!! Please fix this, like, soon!\n')
                await setStatus()
                return
            host = ctx.guild.get_member(host)
            if name == host:
                await sendDebug('Sending react message...')
                reactm = await host.send('Are you sure you want to close the room? React within 15 seconds to confirm.')
                await reactm.add_reaction('☑')
                def check(reaction, user):
                    return reaction.count > 1 and reaction.message.id == reactm.id and str(reaction.emoji) == '☑'
                Permission('I\'ve just asked to make sure they want to...')
                await sendDebug('Sent. Waiting for reaction, or for ten seconds to pass...')
                await bot.wait_for('reaction_add', timeout=15, check=check)
                await reactm.edit(content='Permission was granted.')
                Permission('Permission was granted by the host.')
                await sendDebug('Permission granted. Continuing...')
            else:
                UserErr('They aren\'t the room host, so they can\'t close the room.')
                await name.send('**Sorry, but...** You need to be the room host to do this.')
                await sendDebug('Sender was not room host. Command halted.\n--')
                await setStatus()
                return
        except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
            await sendDebug('Permission was automatically denied. Command halted.\n--')
            await reactm.edit(content='Permission was automatically denied.')
            Permission('No reaction from the host, so permission was automatically denied.\n')
            await setStatus()
            return
        except discord.Forbidden:
            await source.send(dmError)
            await setStatus()
            return
# If permission was granted, I'll start moving users from the room to that floor's lobby.
        await sendDebug('Moving all users to the lobby...')
        counter = 0
        ch = 'lobby-' + str(ctx.message.channel).split('-')[1]
        ch = [a for a in bot.get_all_channels() if a.name == str(ch)]
        while len(source.members) - len(opIDs) > 0: # This will automatically repeat the following process until all users have been removed.
            next = choice(source.members)
            nxid = int(next.id)
            counter = counter + 1
            while nxid in opIDs: # This is so I don't waste time removing any ID found in the "opIDs" list.
                next = choice(source.members)
                nxid = int(next.id)
                counter = counter + 1
# To empty the room, I'll start by taking the user's permissions for the source room.
            await source.set_permissions(next, overwrite=None)
# Next, I'll send a message to the destination room, stating the user has joined.
            response = str(next.mention) + ' has entered the room.'
            await ch[0].send(response)
# Finally, I'll give the user access to the destination room.
            await ch[0].set_permissions(next, overwrite=overwrite)
            await sendDebug('Moved user ' + str(next) + '.')
        Information('All users have been removed. It took ' + str(counter) + ' attempt(s) to remove all users from the room.')
        await sendDebug('Finished in ' + str(counter) + ' attempt(s).')
# Now, I'll recreate the room to clear out the messages.
        pos = int(source.position)
        cch = await source.clone()
        await source.delete()
        await cch.edit(position=pos)
        Success('Room has been closed.')
        await sendDebug('Room closed.\n--')
        await setStatus()
        return

## This command will clear the room - recreating it without removing any users.
@bot.command(name='clear')
async def clear(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!clear\n')
    await sendDebug(str(ctx.message.author) + ' ran command "clear".')
# I need to make sure this was sent in the server.
    if not ctx.guild:
        await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused....')
            UserErr(str(ctx.message.author) + ' tried to clear the room, but sent the command in DMs and not in the server.\n')
            await sendDebug('Command was run in DMs. Halted.\n--')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
        name = ctx.message.author
        source = ctx.message.channel
        dmError = 'Hi, ' + str(name.mention) + '! I tried to send you a DM, but it seems you\'ve disabled the option to allow DMs from server members. You\'ll need to turn that on to host rooms and receive important information from the server.'
# First, I'll check to make sure the room isn't an open room. If so...
        roomName = str(ctx.message.channel).split('-')[0]
        if (roomName in openRooms):
            await sendDebug(':grey_exclamation: The room is open. Command halted.\n--')
            UserErr('This is an open room...\n')
            await setStatus()
            return # ...I'll just stop there and not even bother telling them.
# Otherwise...
# I'll make sure the host wants to clear the room...
        try:
            try:
                with shelve.open('chost') as f:
                    host = f[str(source) + '-host']
            except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                await sendDebug(':x: ' + str(opMention) + '**ERROR:** Room host was not found! Command halted.\n--')
                await name.send('**Eep!** Sorry, I forgot the host of `#' + str(source) + '`... Could you let `' + str(sysop) + '` know? He\'ll be able to fix it!')
                SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this, like, soon!\n')
                await setStatus()
                return
            host = ctx.guild.get_member(host)
            if name == host:
                reactm = await host.send('Are you sure you want to clear the room? React within 15 seconds to confirm.')
                await reactm.add_reaction('☑')
                def check(reaction, user):
                    return reaction.count > 1 and reaction.message.id == reactm.id and str(reaction.emoji) == '☑'
                Permission('I\'ve just asked to make sure they want to...')
                await bot.wait_for('reaction_add', timeout=15, check=check)
                await reactm.edit(content='Permission was granted.')
                Permission('Permission was granted by the host.')
            else:
                await name.send('**Sorry, but...** You need to be the host of the room to do this.')
                UserErr('They weren\'t the host of the room, so they can\'t clear the room.')
                await setStatus()
                return
        except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
            try:
                await reactm.edit(content='Permission was automatically denied.')
                Permission('No reaction from the host, so permission was automatically denied.\n')
            except discord.Forbidden:
                pass
            await setStatus()
            return
        except discord.Forbidden:
            await source.send(dmError)
            await setStatus()
            return
# If permission was granted, I'll recreate the room, then rename the original room to "clearing" so I know to delete the right room.
        pos = int(source.position)
        cch = await source.clone()
        await source.edit(name='clearing')
# Once that's done, I'll start moving everyone there.
        counter = 0
        while len(source.members) - len(opIDs) > 0: # This will automatically repeat the following process until all users have been removed.
            next = choice(source.members)
            nxid = int(next.id)
            counter = counter + 1
            while nxid in opIDs: # This is so I don't waste time removing any ID found in the "opIDs" list.
                next = choice(source.members)
                nxid = int(next.id)
                counter = counter + 1
# To empty the room, I'll start by taking the user's permissions for the source room.
            await source.set_permissions(next, overwrite=None)
# Finally, I'll give the user access to the destination room.
            await cch.set_permissions(next, overwrite=overwrite)
        Information('All users have been removed. It took ' + str(counter) + ' attempt(s) to transfer all users.')
# Now, I'll recreate the room to clear out the messages.
        await source.delete()
        await cch.edit(position=pos)
        Success('Room has been cleared.')
        await setStatus()
        return

# This command will allow the host to lock the room, preventing new users from join the room.
@bot.command(name='lock')
async def lock(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!lock\n')
    await sendDebug(':lock: ' + str(ctx.message.author) + ' ran tnm!lock\n')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
            UserErr(str(ctx.message.author) + ' tried to close the room, but sent the command in DMs and not in the server.\n')
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused....')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
# First, I'll check to make sure the room isn't an open room. If so...
        roomName = str(ctx.message.channel).split('-')[0]
        if (roomName in openRooms):
            UserErr('This is an open room...\n')
            await setStatus()
            return # ...I'll just stop there and not even bother telling them.
# Otherwise...
# Next, I'll check to see if the room is already locked. If it is, I'll say so.
        elif ctx.message.channel.topic == '🔒':
            UserErr('The room is already locked.\n')
            await ctx.message.channel.send('The room is already locked.')
            await setStatus()
            return
# Otherwise...
# All checks have passed, and I can begin.
# The only thing I need to do is adjust the room description.
        else:
            await ctx.message.channel.edit(topic='🔒')
            Success('The room was locked.\n')
            await ctx.message.channel.send('The room was locked.')
            await setStatus()
            return

# This command will allow the host to unlock the room, allowing new people to join.
@bot.command(name='unlock')
async def unlock(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!unlock\n')
    await sendDebug(':unlock: ' + str(ctx.message.author) + ' just ran: tnm!unlock\n')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
        try:
            UserErr(str(ctx.message.author) + ' tried to close the room, but sent the command in DMs and not in the server.\n')
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused....')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
# First, I'll check to make sure the room isn't an open room. If so...
        roomName = str(ctx.message.channel).split('-')[0]
        if (roomName in openRooms):
            UserErr('This is an open room...\n')
            await setStatus()
            return # ...I'll just stop there and not even bother telling them.
# Otherwise...
# Next, I'll check to see if the room is already unlocked. If it is, I'll say so.
        elif ctx.message.channel.topic == '':
            UserErr('The room is already unlocked.\n')
            await ctx.message.channel.send('The room is already unlocked.')
            await setStatus()
            return
# Otherwise...
# All checks have passed, and I can begin.
# The only thing I need to do is adjust the room description.
        else:
            await ctx.message.channel.edit(topic='')
            Success('The room was unlocked.\n')
            await ctx.message.channel.send('The room was unlocked.')
            await setStatus()
            return

## This command allows a user to select a color; after which, I'll assign a role based on said color. Thanks, Color-senpai!~
@bot.command(name='color',alias='colour')
async def color(ctx, hx = '[none]'):
    Information(str(ctx.message.author) + ' just ran: tnm!color ' + str(hx) + '\n')
    await sendDebug(':art: ' + str(ctx.message.author) + ' wants to change their color to ' + str(hx) + '.')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
        try:
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused....')
            UserErr(str(ctx.message.author) + ' tried to change their color, but sent the command in DMs and not in the server.\n')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("color")
        await ctx.message.delete()
# Defining consistent variables here.
        name = ctx.message.author
        sv = ctx.guild
        dmError = 'Hi, ' + str(name.mention) + '! I tried to send you a DM, but it seems you\'ve disabled the option to allow DMs from server members. You\'ll need to turn that on to host rooms and receive important information from the server.'
# First, I'll clean up the input if necessary.
        try:
            hxc = hx.split('#')[1]
        except IndexError: # If there's no #, we don't need to do this.
            hxc = hx
# Now, I'll prepare the input.
        try:
            hxc = int(hxc, 16)
            hxh = hex(hxc)
# If the input is invalid...
        except ValueError:
# ...it may be a color name. Let's check.
            try:
                hxh = getKey(hxc)
# If not...
            except KeyError:
# ...it's time for an error DM!
                try:
                    await sendDebug(':grey_exclamation: A valid input wasn\'t provided. Command halted.\n--')
                    UserErr('They didn\'t provide a valid input.\n\n')
                    await name.send('**Sorry, but...** You need to provide a *valid* input for your desired ' + str(clr) + '. This can be either a ' + str(clr) + ' name or a hex value.')
                except discord.Forbidden:
                    await source.send(dmError)
                await setStatus()
                return
# Once that's done, I'll see if a role for that color exists. If not, I'll create said role.
        try:
            await sendDebug('Getting color role for ' + str(hxc) + ' ready...')
            if hxh in colorset:
                Information(f'The input is in the ' + str(clr) + ' library.')
                colorset.get(hx)
                if colorset[hxh] == 'tooblack':
                    UserErr(f'The ' + str(clr) + ' is too black, but I can fix this!')
                    hx = '010101'
                    hxc = int(hx, 16)
                    hxh = hex(hxc)
                hx = colorset.get(hxh)
                role = [a for a in sv.roles if a.name == 'clr-' + str(hxh)][0]
            else:
                Information(f'The input isn\'t in the ' + str(clr) + ' library.')
                role = [a for a in sv.roles if a.name == 'clr-' + str(hxh)][0]
            await sendDebug('Role ' + str(role) + ' matches.')
            Success(f'Found an associated role. Continuing...')
        except IndexError:
            await sendDebug('No associated role was found. Creating role...')
            Intent('I couldn\'t find the role, so I\'ll need to create it.')
            try:
                if hxh in colorset:
                    hxc = int(getKey(hx), 16)
                role = await sv.create_role(name='clr-' + str(hxh), color=discord.Colour(hxc))
                await sendDebug('Role ' + str(role) + ' was created.')
                Success('Role created. Continuing...')
            except discord.errors.HTTPException:
                await sendDebug(':grey_exclamation: Provided input ended up being out of bounds. Command halted.\n--')
                UserErr('That ended up not working because it\'s invalid...')
                await ctx.message.channel.send('**Sorry, but...** You need to provide a *valid* input for your desired ' + str(clr) + '. This can be either a ' + str(clr) + ' name or a hex value.')
                await setStatus()
                return
# Time to assign the role! First, I'll remove the user from any current color role they have.
        roles = [a for a in name.roles if not a.name.startswith('clr-')] # This ignores any color role the user has.
        roles.append(role)
# Then, I'll give them the new role.
        try:
            await name.edit(roles=roles)
            await sendDebug(':white_check_mark:  Role assigned successfully.')
            Success('The role\'s been assigned!\n')
        except:
            await sendDebug(':grey_exclamation_mark: Application unnecessary.')
            Success('Chances are, they already have that color.\n')
# Finally, I'll delete any unused color roles.
        clroles = [a for a in sv.roles if a.name.startswith('clr-')]
        unused = [a for a in clroles if len(a.members) == 0]
        if len(unused) > 0:
            await sendDebug(':wastebasket: Preparing to delete ' + str(len(unused)) + ' unused roles...')
            Information(str(len(unused)) + ' unused roles need to be deleted.\n')
            await setStatus("busy")
            fofs = 'no'
            counter = 0
            while len(unused) > 0:
                try:
                    next = unused[counter]
                    await next.delete()
                    await sendDebug('Deleted role ' + str(next) + '.')
                    Information(str(next) + ' was deleted.\n')
                    counter = counter + 1
                except discord.errors.NotFound:
                    if fofs == 'no':
                        fofs = 1
                    else:
                        fofs = fofs + 1
                except IndexError:
                    break
            await sendDebug('Successfully deleted ' + str(counter) + ' unused roles, receiving ' + str(fofs) + ' 404 error(s).')
            Success(str(counter) + ' unused role(s) were deleted, with ' + str(fofs) + ' 404 error(s) occurring.\n')
        await setStatus()
        return

## This command will send the user a link to the source code for TNM-chan.
@bot.command(name='source')
async def source(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!source\n')
    if ctx.guild:
        await ctx.message.delete()
    await ctx.message.author.send('The source code for TNM-chan can be found at:\nhttps://github.com/heyitzrare/tnm-chan')

## This command allows the user to view the Boost Software License.
@bot.command(name='license')
async def license(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!license\n')
    if ctx.guild:
        await ctx.message.delete()
    with open('license.txt', 'r') as f:
        bsl = f.read()
    await ctx.message.author.send('```' + str(bsl) + '```')

bot.run(TOKEN)
