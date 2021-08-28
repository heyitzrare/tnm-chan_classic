### TNM-chan ###
### v 21.220 ###

### BEGIN USER-SET VARIABLES ###
# Set your command prefix here.
pre = 'tnm!'

# If you say "colour" instead of "color," change this variable to "True", and I'll change everything accordingly.
useColour = False

# Type your Discord username in quotes, then add your user ID - make sure these are right, because I send both on occasion!
sysop = ''
soID = int()

# Before launching the bot, take note of any moderators that have access to all rooms, and copy their IDs into this list (separated by commas). 
opIDs = [

]

# If you want specific server name formatting, add it in surrounded by either 's or "s.
snFormat = ''

# Type your open room names into this list (separated by commas), surrounded by either 's or "s.
openRooms = [
'lobby',
'entroom'
]

# Choose whether or not you'll use debug commands. If you are, type your debug room's name here.
useDebug = True # Make sure this is a boolean ("True" or "False")!
debugSet = 'bot-debug'

# This is your server's color library. Set some color values here and give them names. Here are the ones in the official server.
colorset = {
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

### END USER-SET VARIABLES ###

    hex(0x000000): 'tooblack', # Don't mess with this entry, it's important! If I try to give the role a pure black color, Discord will replace it with a generic color, which we don't want.
}

# First, I'll import/load libraries.
import traceback
import os
import shelve
import asyncio
from random import choice

### Make sure you've got these modules installed! ###
import termcolor
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

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

if snFormat: # If you set a name for me to use, I'll use that.
    serverName = snFormat
else:
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

# I'll define some constant variables here, as well as a couple more subroutines.
firstConnect = True

overwrite = discord.PermissionOverwrite()
overwrite.send_messages=True
overwrite.read_messages=True

if useColour:
    clr = 'colour'
else:
    clr = 'color'

# Here's how I set my status!~
async def setStatus(type=''):
    if type == "busy":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='with variables'), status=discord.Status.do_not_disturb)
    elif type == "color":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='with colors'), status=discord.Status.idle)
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for "tnm!list"'), status=discord.Status.online)

async def sendDebug(contents):
    if useDebug:
        if firstConnect: # Only here so Rare doesn't have a panic attack. And also to shrink the on_ready function.
            de = [a for a in bot.get_all_channels() if a.name == debugSet]
            debug = de[0]
        try:
            await debug.send(contents)
        except (UnboundLocalError, AttributeError): # If my debug channel variable ever breaks, this will help me reassign it!
            de = [a for a in bot.get_all_channels() if a.name == debugSet]
            debug = de[0]
            await debug.send(contents)
    else:
        pass

# Fancy embed generator time!~
def generateEmbed(clr=0x03FFED,title='[title]',desc='',f1e=0,f1t='[f1t]',f1c='[f1c]',f2e=0,f2t='[f2t]',f2c='[f2c]',f3e=0,f3t='[f3t]',f3c='[f3c]'):
    global embedVal
    embedVal = discord.Embed(
                    title=title, description=desc, color=clr
                )
    if f1e:
        embedVal.add_field(name=f1t, value=f1c, inline=False)
    if f2e:
        embedVal.add_field(name=f2t, value=f2c, inline=False)
    if f3e:
        embedVal.add_field(name=f3t, value=f3c, inline=False)
    return embedVal

# Setting the standard DM messages now, since we couldn't before.
def defaultEmbeds(type, user):
    if type == 'welcome':
        embedVal = generateEmbed(
            title=":tada:  **Hi, " + str(user) + "! Welcome to " + str(serverName) + "!**",
            desc="I'm TNM-chan, your android assistant.\n",
            f1e=1,
            f1t=" You might not know what to do at first, but don't panic!",
            f1c="DM me with `tnm!list`, and I'll send a list of commands your way!")
    elif type == 'welcome_dm':
        embedVal = generateEmbed(
            title=":tada::grey_exclamation: **Hi, " + str(user) + "! Welcome to " + str(serverName) + "!**",
            desc="You're seeing this message because you've disabled direct messages from other server members.\n",
            f1e=1,
            f1t="I send important messages through DMs, specifically if something goes wrong when you use a command.",
            f1c="With that being said, it'd be nice if you could enable DMs from server members, that way I can DM you if something happens. (Don't worry, we won't let anyone spam you!)")
    elif type == 'dmerror':
        embedVal = generateEmbed(
            title=":grey_exclamation: **Hey, " + str(user) + "!**",
            desc="I'm sure you know this already, but you've disabled direct messages from other server members.\n",
            f1e=1,
            f1t="I send important messages through DMs, specifically if something goes wrong with your command.",
            f1c="With that being said, it'd be nice if you could enable DMs from server members, that way I can DM you if something happens. (Don't worry, we won't let anyone spam you!)")
    else:
        return
    return embedVal

# Now I'm ready, so I'll let you know!
Success('I\'m ready to go!')

# If all went well, I'll send a message to the terminal!
@bot.event
async def on_ready():
    DiscordComponents(bot)
    global firstConnect
    global opMention
    global debug
    if firstConnect:
        # Setting up sysop mentions.
        opMention = await bot.fetch_user(int(soID))
        await sendDebug(':green_circle: Connected.')
        Conversion('I\'ve connected to the server!\n')
        firstConnect = False
    else:
        await sendDebug(':blue_circle: Reconnected.')
        Conversion('I got disconnected, but I\'m back online!\n')
    await setStatus()

# Here's how I welcome new users, and get them into #lobby-f1!
@bot.event
async def on_member_join(ctx):
    Intent('Hey! ' + str(ctx) + ' just joined the server.')
    await sendDebug(':new: ' + str(ctx) + ' just joined the server!')
    await setStatus("busy")
    room = [a for a in bot.get_all_channels() if a.name == 'lobby-f1']
    await room[0].set_permissions(ctx, overwrite=overwrite)
    Information('They now have access to #lobby-f1...')
    await sendDebug('Access to #lobby-f1 has been provided...')
    try:
        embedVal = defaultEmbeds('welcome', ctx.mention)
        await ctx.send(embed=embedVal)
        Information('...and the welcome DM\'s been sent.')
        await sendDebug('...and the welcome DM has just been sent.')
    except discord.Forbidden:
        embedVal = defaultEmbeds('welcome_dm', ctx.mention)
        await room[0].send(embed=embedVal)
        UserErr('and I\'ve asked them to enable DMs from server members. Try to make sure they actually do this... ')
        await sendDebug('...and I couldn\'t send the welcome DM, so I just sent a message in lobby-f1.')
    Success('All set!\n')
    await setStatus()
    await sendDebug('All set!\n--')
    
### Okay, here's my commands!

### CORE COMMANDS
## This command allows a user to select a color; after which, I'll assign a role based on said color. Thanks, Color-senpai!~
@bot.command(name='color',aliases=['colour'])
async def color(ctx, hx = '[none]'):
    Information(str(ctx.message.author) + ' wants to change their color to ' + str(hx) + '.\n')
    await sendDebug(':art: ' + str(ctx.message.author) + ' wants to change their color to ' + str(hx) + '.')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        UserErr('The command was sent in DMs, so context can\'t be found.')
        await sendDebug(':grey_exclamation: The command was sent in DMs, so context can\'t be found. Command halted.\n--')
        try:
            UserErr(str(ctx.message.author) + ' tried to change their color, but sent the command in DMs and not in the server.\n')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to set or change your " + str(clr) + ", but sent the command in DMs and not the server.",f1c="As much as I want to, I can't do much if you're not in the server...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the server.",f2c="(Maybe one day, I can do all this cool stuff from in here. One day...)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("color")
        await ctx.message.delete()
        name = ctx.message.author
        sv = ctx.guild
        dmerror = defaultEmbeds('dmerror', name)
# If hx isn't found, I'll assume the user needs help.
        if hx == '[none]':
            await sendDebug(':grey_exclamation: No arg1 provided. Assuming the caller needs assistance....\n--')
            UserErr(str(name) + ' tried to move, but didn\'t provide an arg1. I\'ll assume the caller needs help.\n')
            try:
                embedVal = generateEmbed(title=":grey_question: **Help: ``" + str(pre) + " " + str(clr) + "`**",desc="(You're seeing this message because no arguments were provided.)\n",f1e=1,f1t="This command will let you get a super fancy " + str(clr) + "ed name! In order to help me make your " + str(clr) + " role, you'll need to give me one of two things:",f1c="> A color name that's in our library (click the button below to see a list)\n> A hexadecimal code (e.g. \n",f2e=1,f2t="PLEASE NOTE: I can't set your " + str(clr) + " to `#000000`, as this will remove your " + str(clr) + "!",f2c="Once I have this info, I'll be able to create a " + str(clr) + " role just for you! (And for whoever else decides to use it.)")
            except discord.Forbidden:
                await source.send(embed=dmerror)
            await setStatus()
            return
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
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to set or change your " + str(clr) + ", but provided an invalid input.",f1c="You need to provide a valid hex code or " + str(clr) + " name.\n",f2e=1,f2t="**Solution:** Try running the command again, but make sure your input is valid.",f2c="(If you need help with hex codes, hit up the Internet!)")
                    await ctx.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
                await setStatus()
                return
# Once that's done, I'll see if a role for that color exists. If not, I'll create said role.
        try:
            await sendDebug('Getting color role for ' + str(hxc) + ' ready...')
            if hxh in colorset:
                Information(f'The input is in the ' + str(clr) + ' library.')
                colorset.get(hx)
                if colorset[hxh] == 'tooblack':
                    UserErr(f'The ' + str(clr) + ' is too black - no worries, easy fix!')
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
                embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to set or change your " + str(clr) + ", but provided an invalid code.",f1c="You need to provide a valid hex code - " + str(hxh) + " isn't valid.\n",f2e=1,f2t="**Solution:** Try running the command again, but make sure your " + str(clr) + " code is valid.",f2c="(Hit up the Internet if you need help!)")
                await ctx.send(embed=embedVal)
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

## This command will allow a user to move between specific categories and channels, called "floors" and "rooms" respectively.
@bot.command(name='goto',aliases=['move'])
async def goto(ctx, arg1 = '[none]', arg2 = '[none]'):
    Information(str(ctx.message.author) + ' ran command "goto" with arg1 = `' + str(arg1) + '` and arg2 = `' + str(arg2) + '`.\n')
    await sendDebug(':arrow_forward: ' + str(ctx.message.author) + ' ran command "goto" with arg1 = `' + str(arg1) + '` and arg2 = `' + str(arg2) + '`.')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            UserErr(str(ctx.message.author) + ' tried to move, but sent the command in DMs and not in the server.\n')
            await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to move, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can point you in the right direction...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to move from.",f2c="(For reference, your arg2 (the floor/room you want to move *to*) was `" + str(arg2) + "`.)")
            await ctx.send(embed=embedVal)
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
        dmerror = defaultEmbeds('dmerror', name)

## For floor movement...
        if arg1 == 'floor':
# First, I'll make sure the user didn't forget arg2, and send a DM if they did.
            if arg2 == '[none]':
                await sendDebug(':grey_exclamation: No arg2 provided. Command halted.\n--')
                UserErr(str(name) + ' tried to move, but didn\'t say which floor to move to.\n')
                try:
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to a different floor, but didn't tell me which one.",f1c="I need to know where you wanna go so I can point you in the right direction...\n",f2e=1,f2t="**Solution:** Try running the command again, but specify the floor you want to move to.",f2c="(For reference, there are currently two floors.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
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
                UserErr('They weren\'t in the lobby.\n')
                try:
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to a different floor, but you're not in the lobby.",f1c="The elevators are in the lobby - not literally, but...you get the point.\n",f2e=1,f2t="**Solution:** Run `" + str(pre) + "goto room lobby` and try again.",f2c="(For reference, you tried to move to floor.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
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
                    UserErr('There was no lobby for floor ' + str(arg2.lower()) + ', so it probably doesn\'t exist.\n')
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to a different floor, but I couldn't find a lobby for the floor you wanted.",f1c="That typically means the floor doesn't exist.\n",f2e=1,f2t="**Solution:** Check to make sure your floor exists, then run the command again.",f2c="(If you're certain the floor exists, open a ticket in #support.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
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
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to the floor you wanted to move to.",f1c="I don't need to guide you if you're already in the right place!~\n",f2e=1,f2t="**Solution:** Check to make sure you didn't mistype the floor number. If you did, fix the typo and run the command again.",f2c="(Check #server-info for more information.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
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
        elif arg1 == 'lobby' or arg1 == 'entroom':
            arg2 = str(arg1)
            arg1 = 'room'

        elif arg1 == 'room':
# I need to make sure the user didn't forget arg2, and send a DM if they did.
            if arg2 == '[none]':
                await sendDebug(':grey_exclamation: No arg2 was provided. Command halted.\n--')
                try:
                    UserErr(str(name) + ' tried to move, but didn\'t say which room to move to.\n')
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to a different room, but you didn't tell me which room you wanted to move to.",f1c="(I can't read minds, y'know...)\n",f2e=1,f2t="**Solution:** Run the command again, providing a room name this time.",f2c="(Check #server-info for more information.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
                await setStatus()
                return
# I'll let the terminal know before starting.
            Intent('I\'m starting room movement... ')
            await sendDebug('Starting...')
# First, I'll see if arg2 is just a number (i.e., the command run was "goto room 3").
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
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to the room you wanted to move to.",f1c="I don't need to guide you if you're already in the right place!~\n",f2e=1,f2t="**Solution:** Check to see if you mistyped the room name. If you did, fix the typo and run the command again.",f2c="(Check #server-info for more information.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
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
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to move rooms, but I couldn't find the room you wanted to move to.",f1c="That typically means the room doesn't exist, or you made a typo.\n",f2e=1,f2t="**Solution:** Check to make sure your room exists (and that you spelled it properly), then run the command again.",f2c="(For reference, you typed `" + str(arg2.lower()) + "`. If you're certain the room exists, open a ticket in #support.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
                await setStatus()
                return
# Otherwise...
# Next, I'll make sure the room isn't locked.
            if newch[0].topic == '🔒':
# If it is, I'll let them know.
                await sendDebug(':grey_exclamation: The room they tried to move to is locked. Command halted.\n--')
                try:
                    Information('The room is locked.')
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to move to " + str(arg2) + ", but the room was locked. ",f1c="That means the host of the room doesn't want anyone else to join the room.\n",f2e=1,f2t="**Solution:** Check out some of the other rooms, or contact the room's host.",f2c="(Check #server-info for more information. If the host is camping the room, open a ticket in #support.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
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
                            embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                            await name.send(embed=embedVal)
                            embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `chost.dat`.",f1c="Check to make sure the file is present.")
                            await opMention.send(embed=embedVal)
                            await setStatus()
                            return
                        host = ctx.guild.get_member(host)
                        # New function to pass a note over to the host!
                        embedVal = generateEmbed(title='The current room host is ' + str(host) + '.',desc='Want me to pass a note to them?')
                        await sendDebug('Asking if the user wants to send a note...')
                        Intent('Asking if the user wants to send a note...')
                        msg = await name.send(
                            embed=embedVal,
                            components = [
                                [
                                    Button(style=ButtonStyle.blue, label="Sure!"),
                                    Button(style=ButtonStyle.grey, label="No thanks.")
                                ]
                            ]
                        )
                        state = await bot.wait_for('button_click')
                        if state.component.label == "Sure!":
                            time = 90
                            sendNote = True
                            embedVal = generateEmbed(title='Go ahead and type a note for me to pass to ' + str(host) + '.',desc='Try to type it quickly, I\'ve probably got other people to help out...')
                            Intent('Waiting on a note...')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )
                            def check(message: discord.Message):
                                return message.author == name
                            notemsg = await bot.wait_for('message', check=check)
                            noteContents = notemsg.content
                            Intent('Note "' + str(noteContents) + '" received!')
                            embedVal = generateEmbed(clr=0x33ff00,title='Got it. I\'ll send the request right away!',desc='')
                            await msg.edit(embed=embedVal)
                        else:
                            time = 30
                            sendNote = False
                            Intent('They chose not to send a note.')
                            embedVal = generateEmbed(clr=0x33ff00,title='Got it. I\'ll send the request right away!',desc='')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )

                        # Now I can send the confirmation message to the host!
                        await sendDebug('Sending the confirmation message...')
                        if sendNote:
                            embedVal = generateEmbed(title=str(name) + ' wants to join ' + str(source) + '.',desc='They wanted me to pass this note to you:```' + str(noteContents) + '```',f1e=1,f1t='Click or tap a button within ' + str(time) + ' seconds.',f1c='If no reaction is received, permission will be denied automatically.')
                        else:
                            embedVal = generateEmbed(title=str(name) + ' wants to join ' + str(source) + '.',desc='They didn\'t want me to pass a note.',f1e=1,f1t='Click or tap a button within ' + str(time) + ' seconds.',f1c='If no reaction is received, permission will be denied automatically.')
                        msg = await host.send(
                            embed=embedVal,
                            components = [
                                [
                                    Button(style=ButtonStyle.green, label="Accept"),
                                    Button(style=ButtonStyle.grey, label="Deny")
                                ]
                            ]
                        )
                        Intent('I\'ve just asked for permission.')
                        await sendDebug('I\'ve just asked for permission. I\'m now waiting for activity within ' + str(time) + ' seconds...')
                        state = await bot.wait_for('button_click', timeout=time)
                        if state.component.label == "Accept":
                            embedVal = generateEmbed(clr=0x33ff00,title='You granted me permission to add ' + str(name) + ' to ' + str(source) + '.',desc='')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )
                            Success('Permission was granted by the host.')
                            await sendDebug('Permission granted. Continuing...')
                        else:
                            embedVal = generateEmbed(clr=0xff4444,title='You denied me permission to add ' + str(name) + ' to ' + str(source) + '.',desc='')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )
                            UserErr('Permission was denied by the host.')
                            await sendDebug('Permission was denied. Command halted.\n--')
                            embedVal = generateEmbed(clr=0xff4444,title=":no_entry_sign: **The host denied you access...**",desc="Why not see if another room is available?\n")
                            await name.send(embed=embedVal)
                            await setStatus('')
                            return
                    except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
                        await sendDebug('Permission was automatically denied. Command halted.\n--')
                        try:
                            embedVal = generateEmbed(clr=0x777777,title='You didn\'t react in time, so ' + str(name) + ' won\'t be added to ' + str(source) + '.',desc='')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )
                            UserErr('No reaction from the host, so permission was automatically denied.\n')
                            embedVal = generateEmbed(clr=0x777777,title=":clock3: **The host didn't react to the message...**",desc="Try sending them another request when you know they're available.\n")
                            await name.send(embed=embedVal)
                        except discord.Forbidden:
                            await source.send(embed=dmerror)
                        await setStatus('')
                        return
                    except discord.Forbidden:
                        await source.send(embed=dmerror)
                        await setStatus('')
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
                        embedVal = generateEmbed(title=":house: **You're the host of " + str(arg2.lower) + "!**",desc="If somebody tries to join, I'll send you a DM letting you know.\n")
                        await name.send(embed=embedVal)
                    except discord.Forbidden:
                        await source.send(embed=dmerror)
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
                    embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something's gone wrong with my code itself...",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                    await name.send(embed=embedVal)
                    SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this!\n')
                    embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something's gone wrong with my code itself...",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `chost.dat`.",f1c="Check to make sure the file is present.")
                    await opMention.send(embed=embedVal)
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
                            await sendDebug('This user can\'t be the host. Trying again...')
                            print(nhid)
                        with shelve.open('chost') as f:
                            chost = {}
                            f[str(source) + '-host'] = int(nhid)
                        await sendDebug('Operation completed after ' + str(counter) + ' attempt(s).')
                        nhst = ctx.guild.get_member(newhost)
                        await sendDebug('New room host is ' + str(nhst) + '.')
                        embedVal = generateEmbed(title=":house: **You're now the host of " + str(arg2.lower) + "!**",desc="If somebody tries to join, I'll send you a DM letting you know.\n")
                        await nhst.send(embed=embedVal)
                        Intent(str(name) + ' is leaving, so I made ' + str(newhost) + 'the room\'s new host. It took ' + str(counter) + ' attempt(s) to select them.')
                    except discord.Forbidden:
                        await source.send(embed=dmerror)
                        await setStatus()
                        return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source room...
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
            await sendDebug('Source perms taken.')
# ...and giving them access to the destination room.
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
            await sendDebug(':grey_exclamation: No arg1 provided, so I\'ll assume the caller needs help...\n--')
            UserErr(str(name) + ' tried to move, but didn\'t provide an arg1. I\'ll assume the caller needs help.\n')
            try:
                embedVal = generateEmbed(title=":grey_question:  **Help: ``" + str(pre) + "goto`**",desc="(You're seeing this message because no arguments were provided.)\n",f1e=1,f1t="This command will help me guide you around the Mansion! In order for me to know where you wanna go, you'll need to tell me the following:",f1c="> Whether or not you want to go to a `floor` or a `room`\n> If you want to move to a floor, provide a floor number\n> If you want to move to a room, provide a room name\n",f2e=1,f2t="PLEASE NOTE: If you want to move floors, make sure you're in the lobby before moving!",f2c="Once I have this info, I'll be able to get you to where you need to go!")
                await ctx.send(embed=embedVal)
            except discord.Forbidden:
              await source.send(embed=dmerror)
            await setStatus('')
            return
# Or, if they mistyped arg1...
        else:
            await sendDebug(':grey_exclamation: Invalid arg1 provided. Command halted.\n--')
            try:
                UserErr(str(name) + ' tried to move, but provided an invalid arg1. They tried to use "' + str(arg1) + '".\n')
                embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** Your arg1 (`" + str(arg1) + "`) wasn't a valid option. ",f1c="Maybe there's a typo in there somewhere?\n",f2e=1,f2t="**Solution:** Run the command again, but make sure to use either `floor` or `room` as your arg1.",f2c="(Check the #about channel for more information.)")
                await name.send(embed=embedVal)
            except discord.Forbidden:
                await source.send(embed=dmerror)
            await setStatus()
            return


### ROOM COMMANDS
## This command will clear the room - recreating it without removing any users.
@bot.command(name='clear')
async def clear(ctx):
    Information(str(ctx.message.author) + ' wants to clear the room they\'re in.\n')
    await sendDebug(str(ctx.message.author) + ' wants to clear the room they\'re in.')
# I need to make sure this was sent in the server.
    if not ctx.guild:
        await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            UserErr(str(ctx.message.author) + ' tried to clear the room, but sent the command in DMs and not in the server.\n')
            await sendDebug('Command was run in DMs. Halted.\n--')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to clear the room you're in, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can figure out what room to clear...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to clear.",f2c="(Maybe one day, I can clear a room from in here. One day...)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
        name = ctx.message.author
        source = ctx.message.channel
        dmerror = defaultEmbeds('dmerror', name)
# First, I'll check to make sure the room isn't an open room. If so...
        roomName = str(ctx.message.channel).split('-')[0]
        if (roomName in openRooms):
            UserErr('This is an open room...\n')
            await ctx.send('This is an open room...')
            await setStatus()
            return
# Otherwise...
# I'll make sure the host wants to clear the room...
        try:
            try:
                with shelve.open('chost') as f:
                    host = f[str(source) + '-host']
            except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                await sendDebug(':x: ' + str(opMention) + '**ERROR:** Room host was not found! Command halted.\n--')
                SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this, like, soon!\n')
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                await name.send(embed=embedVal)
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `chost.dat`.",f1c="Check to make sure the file is present.")
                await opMention.send(embed=embedVal)
                await setStatus()
                return
            host = ctx.guild.get_member(host)
            await sendDebug('Sending the reaction message...')
            embedVal = generateEmbed(title='Are you *sure* you want to clear ' + str(source) + '?',desc='Click or tap a button within 30 seconds.')
            msg = await host.send(
                embed=embedVal,
                components = [
                    [
                        Button(style=ButtonStyle.grey, label="Cancel"),
                        Button(style=ButtonStyle.red, label="Clear")
                    ]
                ]
            )
            Intent('I\'ve just asked for permission.')
            await sendDebug('I\'ve just asked for permission. I\'m now waiting for activity within 30 seconds...')
            state = await bot.wait_for('button_click', timeout=30)
            if state.component.label == "Clear":
                embedVal = generateEmbed(clr=0xff4444,title='You granted me permission to clear ' + str(source) + '.',desc='')
                await msg.edit(
                    embed=embedVal,
                    components = []
                )
                Success('Permission was granted by the host.')
                await sendDebug('Permission granted. Continuing...')
            else:
                embedVal = generateEmbed(clr=0x777777,title='You denied me permission to clear ' + str(source) + '.',desc='')
                await msg.edit(
                    embed=embedVal,
                    components = []
                )
                UserErr('Permission was denied by the host.')
                await sendDebug('Permission was denied. Command halted.\n--')
                await setStatus('')
                return
        except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
            await sendDebug('Permission was automatically denied. Command halted.\n--')
            try:
                embedVal = generateEmbed(clr=0x777777,title='You didn\'t react to the message, so I automatically cancelled the clearing operation.' + str(source) + '.',desc='')
                await msg.edit(
                    embed=embedVal,
                    components = []
                )
                UserErr('No reaction from the host, so permission was automatically denied.\n')
            except discord.Forbidden:
                await source.send(embed=dmerror)
            await setStatus('')
            return
        except discord.Forbidden:
            await source.send(embed=dmerror)
            await setStatus('')
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
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to close the room you're in, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can figure out what room to close...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to close.",f2c="(Maybe one day, I can close a room from in here. One day...)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await setStatus("busy")
        await ctx.message.delete()
        source = ctx.message.channel
        name = ctx.message.author
        dmerror = defaultEmbeds('dmerror', name)
# First, I'll check to make sure the room isn't an open room. If so...
        roomName = str(source).split('-')[0]
        if (roomName in openRooms):
            UserErr('This is an open room...\n')
            await ctx.send('This is an open room...')
            await setStatus()
            return
# Otherwise...
# I'll make sure the host wants to close the room...
        try:
            try:
                with shelve.open('chost') as f:
                    host = f[str(source) + '-host']
            except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                await sendDebug(':x: ' + str(opMention) + '**ERROR:** Room host was not found! Command halted.\n--')
                SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this, like, soon!\n')
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                await name.send(embed=embedVal)
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `chost.dat`.",f1c="Check to make sure the file is present.")
                await opMention.send(embed=embedVal)
                await setStatus()
                return
            host = ctx.guild.get_member(host)
            await sendDebug('Sending the reaction message...')
            embedVal = generateEmbed(title='Are you *sure* you want to close ' + str(source) + '?',desc='Click or tap a button within 30 seconds.')
            msg = await host.send(
                embed=embedVal,
                components = [
                    [
                        Button(style=ButtonStyle.grey, label="Cancel"),
                        Button(style=ButtonStyle.red, label="Close")
                    ]
                ]
            )
            Intent('I\'ve just asked for permission.')
            await sendDebug('I\'ve just asked for permission. I\'m now waiting for activity within 30 seconds...')
            state = await bot.wait_for('button_click', timeout=30)
            if state.component.label == "Close":
                embedVal = generateEmbed(clr=0xff4444,title='You granted me permission to close ' + str(source) + '.',desc='')
                await msg.edit(
                    embed=embedVal,
                    components = []
                )
                Success('Permission was granted by the host.')
                await sendDebug('Permission granted. Continuing...')
            else:
                embedVal = generateEmbed(clr=0x777777,title='You denied me permission to close ' + str(source) + '.',desc='')
                await msg.edit(
                    embed=embedVal,
                    components = []
                )
                UserErr('Permission was denied by the host.')
                await sendDebug('Permission was denied. Command halted.\n--')
                await setStatus('')
                return
        except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
            await sendDebug('Permission was automatically denied. Command halted.\n--')
            try:
                embedVal = generateEmbed(clr=0x777777,title='You didn\'t react to the message, so I automatically cancelled the closing operation.' + str(source) + '.',desc='')
                await msg.edit(
                    embed=embedVal,
                    components = []
                )
                UserErr('No reaction from the host, so permission was automatically denied.\n')
            except discord.Forbidden:
                await source.send(embed=dmerror)
            await setStatus('')
            return
        except discord.Forbidden:
            await source.send(embed=dmerror)
            await setStatus('')
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
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to lock the room you're in, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can figure out what room to lock...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to lock.",f2c="(Maybe one day, I can lock a room from in here. One day...)")
            await ctx.send(embed=embedVal)
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
            await ctx.send('This is an open room...')
            await setStatus()
            return
# Otherwise...
# Next, I'll check to see if the room is already locked. If it is, I'll say so.
        if ctx.message.channel.topic == '🔒':
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
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to unlock the room you're in, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can figure out what room to unlock...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to unlock.",f2c="(Maybe one day, I can unlock a room from in here. One day...)")
            await ctx.send(embed=embedVal)
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
            await ctx.send('This is an open room...')
            await setStatus()
            return
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


## OTHER COMMANDS ##
## This command allows the user to view the Boost Software License.
@bot.command(name='license',aliases=['bsl'])
async def license(ctx):
    Information(str(ctx.message.author) + ' just ran: tnm!license\n')
    if ctx.guild:
        await ctx.message.delete()
    embedVal = discord.Embed(title=':page_facing_up: **Boost Software License**', description='TNM-chan is licensed under the Boost Software License, which gives you specific rights to the source code. Click the button below to view the License in your browser.')
    await ctx.message.channel.send(embed=embedVal,
components = [
    [
        Button(style=ButtonStyle.URL, label="View in Browser", url='https://github.com/heyitzrare/tnm-chan/blob/master/LICENSE.TXT')
    ]
            ]
)

## Here's a command list. Remember, more details are given when the commands are run.
@bot.command(name='list',aliases=['help'])
async def list(ctx):
    Information(str(ctx.message.author) + ' just requested the command list.\n')
    if ctx.guild:
        await ctx.message.delete()
    embedVal = discord.Embed(color=0x03FFED, title=':grey_question:  **Command List**',
    description='Prefix your command with `' + str(pre) + '` to run the command. Commands may be added, altered, or removed in the future.\n--')

    embedVal.add_field(name='Core Commands',
    value='**Note:** To get help, run the command without arguments.\n> **' + str(clr) + ':** Creates a unique ' + str(clr) + ' role for your name. (Both forms of ' + str(clr) + ' work, so don\'t worry about that being an issue!)\n> **goto/move:** Move between floors/rooms.', inline=False)
    
    embedVal.add_field(name='Room Commands',
    value='**Note:** You *must* be the room host to use these commands.\n> **clear:** Deletes all messages in a room without moving members.\n> **close:** Deletes all messages in a room and moves all members back to the lobby.\n> **lock|unlock:** Locks or unlocks a room.', inline=False)
    
    embedVal.add_field(name='Other Commands',
    value='> **license/bsl:** Sends a copy of the Boost Software License.\n> **list/help:** Brings up a list of commands.\n> **source/github:** Sends a link to my source code, that way you can see what makes me tick!', inline=False)
    try:
        await ctx.message.author.send(embed=embedVal)
    except discord.Forbidden:
        embedVal.add_field(
            name='***Please* enable DMs from server members...**',
            value="I'd prefer to send stuff like this in DMs, as to not create unnecessary clutter in the server. That said, could you enable DMs from server members, please? It'd make me happy!"
        )
        try:
            await ctx.message.channel.send(embed=embedVal)
        except:
            pass

## This command will send the user a link to the source code for TNM-chan.
@bot.command(name='source',aliases=['github'])
async def source(ctx):
    Information(str(ctx.message.author) + ' ran: ' + str(pre) + 'source\n')
    if ctx.guild:
        await ctx.message.delete()
    embedVal = generateEmbed(title=":desktop: You can find my source code here!",desc="https://github.com/heyitzrare/tnm-chan")
    await ctx.message.channel.send(embed=embedVal)

bot.run(TOKEN)
