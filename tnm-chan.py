### TNM-chan ###
### v 22.051 ###

import configparser
import os
import subprocess
import sys
from datetime import datetime

global firstConnect
firstConnect = True

# Color-coded logging! I see this as an absolute win.
if firstConnect: # Done so we can roll this up in cool code editors.
    def Information(m): print(str(datetime.now()) + "\033[97m {}\033[00m" .format(m)) # Gray

    def Success(m): print(str(datetime.now()) + "\033[92m {}\033[00m" .format(m)) # Green

    def UserErr(m): print(str(datetime.now()) + "\033[93m {}\033[00m" .format(m)) # Yellow
    def SysErr(m): print(str(datetime.now()) + "\033[91m {}\033[00m" .format(m)) # Red

    def Permission(m): print(str(datetime.now()) + "\033[95m {}\033[00m" .format(m)) # Purple
    def Network(m): print(str(datetime.now()) + "\033[34m {}\033[00m" .format(m)) # Blue
    def Highlight(m): print(str(datetime.now()) + "\033[96m {}\033[00m" .format(m)) # Cyan

if firstConnect: # Clearing the screen to start the terminal, and it changes based on what OS you're running! Woo!
    os.system('cls') if os.name == 'nt' else os.system('clear')
    Highlight('TNM-chan is starting...')
    modulesUnloaded = True

def refreshSettings():
    try: # Let's start by grabbing your settings and color presets!
        if firstConnect:
            global cfg
        cfg = configparser.ConfigParser()
        Information('Loading system settings...')
        cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_settings.ini'))
    except FileNotFoundError: # If I can't find the '_settings.ini' file, I'll automatically close myself.
        SysErr("ERROR: The \"_settings.ini\" file couldn't be located - please make sure you've downloaded the entire repository!")
        Information('A fatal error has occurred. TNM-chan will now close.')
        sys.exit(-1)

    if firstConnect:
        global getVar
    def getVar(var, ini='UserSettings'):
        return cfg.get(ini, var)

    if firstConnect:
        global pre, serverName, useColour, startRoom, sysop, useDebug, debugRoom, TOKEN # Globalized these so we can actually save them.
        TOKEN = getVar('token') # I only need this one time.
    pre = getVar('Prefix')
    serverName = getVar('ServerName')
    useColour = getVar('UseColour?')
    startRoom = getVar('StartChannel')
    sysop = getVar('SysOp')
    useDebug = getVar('UseDebug?')
    debugRoom = getVar('DebugChannel').split('#')[1]

    if firstConnect:
        global opIDs, namedRooms, openRooms
    opIDs = list(getVar('GlobalIDs').split(", "))
    namedRooms = list(getVar('NamedChannels').split(", "))
    openRooms = list(getVar('OpenChannels').split(", "))

    cfg.remove_section('UserSettings')

def reloadColorSet():
    if firstConnect:
        global colorset
    try: # Now, I'll load your color presets (which I refer to as a "color set") using the same method I loaded the system settings.
        Information('Loading color presets...')
        cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_colorset.ini'))
        colorset = dict(cfg.items('ColorSet'))
        cfg.remove_section('ColorSet')
    except: # If I can't find the '_colorset.ini' file, or the module breaks, I'll just skip adding it and add "tooblack" to an empty color set.
        UserErr("WARNING: The \"_colorset.ini\" file couldn't be located, or isn't set up properly! Please make sure you've downloaded the entire repository, or make sure the first four lines are EXACTLY like they are in the repository version!")
        Information('Since a color set couldn\'t be used, members won\'t be able to use presets.')
        colorset = {}
    cslen = len(colorset) 
    colorset[hex(0x000000)] = 'tooblack' # If I try to give a role a pure black color, Discord will replace it with...nothing. I'll use this as a pointer to fix that if necessary.
    if cslen == 0:
        Highlight('No color presets to import...')
    elif cslen == 1:
        Highlight("Imported 1 color preset.")
    else:
        Highlight(f"Imported {str(cslen)} color presets.")
    return cslen

refreshSettings()
reloadColorSet()

def getKey(val): # Here's a trick for using a color name to grab a hex value!
    for key, value in colorset.items(): 
        if val == value: 
            return key
    raise KeyError()

Information('Importing more modules...')

# The first modules I'll import are core libraries you shouldn't need to install.
import traceback
import asyncio
from random import choice

uninit = True # The first thing I want to do is make sure discord.py and DiscordComponents are installed.
newlyInstalled = False
while uninit == True:
    try:
        import discord
        from discord.ext import commands
        from discord_components import DiscordComponents, Button, ButtonStyle
        uninit = False
        del newlyInstalled
    except:
        if newlyInstalled == True: # If I've already tried installing termcolor in this session, and I still can't find it...
            Information("I couldn't import discord.py and/or DiscordComponents. You might need to run the script again.")
            sys.exit(0)
        else:
            UserErr("WARNING: One or both of the required modules aren't present.")
            Network("I'll go ahead and install these before I can continue...")
            scmd = 'pip install -U discord.py discord_components'
            subprocess.run(scmd,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            newlyInstalled = True
            Success('Module(s) installed! I\'ll try importing them again...')

Information('Getting ready to authenticate with Discord...')

# Due to a new Discord requirement, I need to set up intents now. Thanks, Discord.
intents = discord.Intents.all()

# I'll arm my prefix and remind Discord of what I want to do.
bot = commands.Bot(command_prefix=str(pre), intents=intents)

# I'll remove the default "help" command so I can use my own.
bot.remove_command('help')

Information('Generating some things I couldn\'t before...')

# I'll define some constant variables here, as well as a couple more subroutines.

overwrite = discord.PermissionOverwrite()
overwrite.send_messages = True
overwrite.read_messages = True

if useColour:
    clr = 'colour'
else:
    clr = 'color'

global path
path = os.path.realpath(__file__).strip(os.path.basename(__file__))

def hostIni(x, a1=None, a2=None): # This will allow me to assign a host to a given room using a human-readable .ini file.

    ### HOW TO USE ###
    # The number to the left is "x," which is our action code.
    # 0 | CREATEs the "hosts.ini" file if it isn't already there.
    # 1 | READs the host of the room "a1" calls for.
    # 2 | UPDATEs the host of the room "a1" calls for to the username "a2" provides.

    path = os.path.abspath(__file__).split(os.path.basename(__file__))[0]
    ini = 'RoomHosts'
    if not os.path.isdir(path + 'system'):
        os.mkdir(path + 'system')
        Information('Created the "/system" subdirectory.')
    path = os.path.join(path + 'system\hosts.ini')
    if not os.path.exists(path): # If I can't find hosts.ini...
        if x == 0: # ...and I can create the file, I'll do that.
            Information('Creating "hosts.ini"...')
            with open(path,'w') as f:
                f.write('[RoomHosts]\n')
            Highlight('Created "hosts.ini" successfully!')
            return
        else: # If creation is disabled...
            UserErr('WARNING: I couldn\'t find the "hosts.ini" file! Was it somehow deleted?')
            raise(FileNotFoundError) # ...I'll throw this instead.
    
    if x == 1: # Reads the host of the room "a1" calls for.
        if a1 is None: # If you forget to tell me what room to check...
            SysErr("ERROR: I don't know what room to check the host of!")
            return # ...I'll return nothing instead.
        cfg.read(path)
        try: # We can grab the host of the room and return it in one line!
            return int(getVar(r'{}'.format(a1), ini))
        except configparser.NoOptionError: # If a1 doesn't exist...
            return # ...I'll return nothing instead.

    elif x == 2: # Updates the host of the room "a1" calls for to the username "a2" provides.
        if a1 is None or a2 is None: # If you forget one or both arguments...
            SysErr("ERROR: One or both necessary arguments weren't provided!")
            return # ...I'll return nothing instead.
        cfg.read(path)
        if cfg.has_option(ini,a1):
            cfg.remove_option(ini,a1)
        if a2 is not 'del':
            a2 = str(a2)
            cfg.set(ini, a1, a2)
        with open(path,'w') as r:
            cfg.write(r)
        return

    elif x == 0: # Remember, if "hosts.ini" already exists...
        if a1:
            Information('Deleting and recreating "hosts.ini"...')
            os.remove(path)
            with open(path,'w') as f:
                f.write('[RoomHosts]\n')
            Highlight('Recreated "hosts.ini" successfully!')
        else:
            Information('The "hosts.ini" file already exists.')
            return # ...I don't need to create it again.
    else:
        SysErr('ERROR: Invalid action code! The provided action code was "' + x + '".')
        return

Information('Checking if "hosts.ini" exists...')
hostIni(0)

def generateEmbed(clr=0x03FFED, title='[title]', desc='', f1e=0, f1t='[f1t]', f1c='[f1c]', f2e=0, f2t='[f2t]', f2c='[f2c]' ,f3e=0, f3t='[f3t]' ,f3c='[f3c]'):
    global embedVal # Fancy embed generator time! Wooooooooo-
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

def defaultEmbeds(type, user): # Setting the standard DM messages now, since we couldn't before.

    user = str(user).split('#')[0]
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

async def sendDebug(contents): # This subroutine handles debug output in the server - this can't be disabled on the terminal.
    if useDebug:
        if firstConnect: # Only here so Rare doesn't have a panic attack. And also to shrink the on_ready function.
            de = [a for a in bot.get_all_channels() if a.name == debugRoom]
            debug = de[0]
        try:
            await debug.send(contents)
        except (UnboundLocalError, AttributeError): # If my debug channel variable ever breaks, I can reassign it and try again.
            de = [a for a in bot.get_all_channels() if a.name == debugRoom]
            debug = de[0]
            await debug.send(contents)

async def setStatus(type=''): # Here's how I set my status to tell you what I'm doing!
    if type == "busy":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='with variables'), status=discord.Status.do_not_disturb)
    elif type == "color":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='with colors'), status=discord.Status.idle)
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for "tnm!help"'), status=discord.Status.online)


# Now I'm ready, so I'll let you know!
Network('All set! I\'m connecting to your server...')

# Once I get online (be it for the first time or after a reconnect), I'll send a message to the terminal!
@bot.event
async def on_ready():
    global firstConnect
    global staffRole
    DiscordComponents(bot)
    global opUser
    opUser = await bot.fetch_user(int(sysop))
    global debug
    if firstConnect:
        await sendDebug(':green_circle: Connected.')
        Success('Connected!\n')
        firstConnect = False
    else:
        await sendDebug(':blue_circle: Reconnected.')
        Highlight('I got disconnected, but I\'m back online!\n')
    await setStatus()

# Here's how I welcome new users, and get them into #lobby-f1!
@bot.event
async def on_member_join(ctx):
    Highlight(str(ctx) + ' just joined the server!')
    await sendDebug(':new: ' + str(ctx) + ' just joined the server!')
    await setStatus("busy")
    room = [a for a in bot.get_all_channels() if a.name == startRoom]
    await room[0].set_permissions(ctx, overwrite=overwrite)
    Information('They now have access to ' + startRoom + '...')
    await sendDebug('They now have access to ' + startRoom + '...')
    try:
        embedVal = defaultEmbeds('welcome', ctx)
        await ctx.send(embed=embedVal)
        Information('...and I just sent the welcome DM.')
        await sendDebug('...and I just sent the welcome DM.')
    except discord.Forbidden:
        embedVal = defaultEmbeds('welcome_dm', ctx)
        await room[0].send(embed=embedVal)
        UserErr('...and I couldn\'t send the welcome DM, so I just sent a message in lobby-f1.')
        await sendDebug('...and I couldn\'t send the welcome DM, so I just sent a message in lobby-f1.')
    Success('All set!\n')
    await setStatus()
    await sendDebug(':white_check_mark: All set!\n--')


### CORE COMMANDS
@bot.command(name='color',aliases=['colour'])
async def color(ctx, hx = '[none]'): ## This command allows a user to select a color; after which, I'll assign a role based on said color. Thanks, Color-senpai!~
    Information(str(ctx.message.author) + ' wants to change their color to ' + str(hx) + '.')
    await sendDebug(':art: ' + str(ctx.message.author) + ' wants to change their color to ' + str(hx) + '.')
    if not ctx.guild: # I need to make sure this was sent in the server. If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        UserErr('The command was sent in DMs, so context can\'t be found.\n')
        await sendDebug(':grey_exclamation: The command was sent in DMs, so context can\'t be found. Command halted.')
        try:
            UserErr(str(ctx.message.author) + ' tried to change their color, but sent the command in DMs and not in the server.\n')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to set or change your " + clr + ", but sent the command in DMs and not the server.",f1c="As much as I want to, I can't do much if you're not in the server...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the server.",f2c="(Maybe one day, I can do all this cool stuff from in here. One day...)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return
    else: # Otherwise, I'll start the command!
        await setStatus("color")
        await ctx.message.delete()
        name = ctx.message.author
        sv = ctx.guild
        dmerror = defaultEmbeds('dmerror', name)

        if hx == '[none]': # If hx isn't found, I'll assume the user needs help.
            await sendDebug(':grey_exclamation: Nothing was provided, so I think they need help.')
            UserErr('Nothing was provided, so I think they need help.\n')
            try:
                embedVal = generateEmbed(title=":grey_question: **Help: `" + str(pre) + " " + clr + "`**",desc="(You're seeing this message because no arguments were provided.)\n",f1e=1,f1t="This command will let you get a super fancy " + clr + "ed name! In order to help me make your " + clr + " role, you'll need to give me one of two things:",f1c="> A color name that's in our library\n> A hexadecimal code\nYou can also type `remove` to get rid of your " + clr + " role.",f2e=1,f2t="Once I have this info, I'll be able to create a " + clr + " role just for you! (And for whoever else decides to use it.)",f2c="Alternatively, if you decide to remove your " + clr + " role, it'll simply be removed (and deleted if nobody else is using it).")
            except discord.Forbidden:
                await source.send(embed=dmerror)
            await setStatus()
            return

        if hx not in ['remove', 'reset', 'tooblack']: # Let's set up the role! We're skipping this if the caller wants their role removed.
            try: # First, I'll clean up the input if necessary.
                hxc = hx.split('#')[1]
            except IndexError: # If there's no #, we don't need to do this.
                hxc = hx
            try: # Now, I'll prepare the input.
                hxc = int(hxc, 16)
                hxh = hex(hxc)
            except ValueError: # If the input is invalid...
                try:
                    hxh = getKey(hxc) # ...it may be a color name. Let's check.
                except KeyError: # If not...
                    try: # ...the provided input isn't valid, so it's error DM time!
                        await sendDebug(':grey_exclamation: A valid input wasn\'t provided. Command halted.\n--')
                        UserErr('They didn\'t provide a valid input.\n\n')
                        embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to set or change your " + clr + ", but provided an invalid input.",f1c="You need to provide a valid hex code or " + clr + " name. (You can also type `remove` to get rid of your " + clr + " role.)\n",f2e=1,f2t="**Solution:** Try running the command again, but make sure your input is valid.",f2c="(If you need help with hex codes, online resources are a good place to start!)")
                        await ctx.send(embed=embedVal)
                    except discord.Forbidden:
                        await source.send(embed=dmerror)
                    await setStatus()
                    return

            try: # Once that's done, I'll see if a role for that color exists.
                if hxh in colorset:
                    Information(f'The input is in the ' + clr + ' library.')
                    colorset.get(hx)
                    if colorset[hxh] == 'tooblack':
                        Information(f'The ' + clr + ' is too black - no worries, easy fix!')
                        hx = '010101'
                        hxc = int(hx, 16)
                        hxh = hex(hxc)
                    hxl = colorset.get(hxh)
                    role = [a for a in sv.roles if a.name == 'clr-' + str(hxc)][0]
                else:
                    Information(f'The input isn\'t in the ' + clr + ' library.')
                    role = [a for a in sv.roles if a.name == 'clr-' + str(hxc)][0]
                await sendDebug('Role ' + str(role) + ' matches.')
                Success(f'Found an associated role. Continuing...')
            except IndexError: # This is generally what happens, but if I can't find the role...
                await sendDebug('I couldn\'t find the role, so I\'ll need to create it.')
                Information('I couldn\'t find the role, so I\'ll need to create it.')
                try: # ...I'll need to create it.
                    if hxh in colorset:
                        hxc = int(getKey(hxl), 16)
                    role = await sv.create_role(name='clr-' + str(hxc), color=discord.Colour(hxc))
                    await sendDebug('Role ' + str(role) + ' was created.')
                    Success('Role ' + str(role) + ' was created. Continuing...')
                except discord.errors.HTTPException:
                    await sendDebug(':grey_exclamation: That ended up not working because the input was out of bounds... Command halted.\n--')
                    UserErr('That ended up not working because the input was out of bounds...')
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to set or change your " + clr + ", but the provided input was out of bounds.",f1c="Make sure to provide a valid hex code - `" + str(hx) + "` likely *isn't* valid.\n",f2e=1,f2t="**Solution:** Try running the command again, but make sure the hex code is valid.",f2c="(If you need help, why not look online?)")
                    await ctx.send(embed=embedVal)
                    await setStatus()
                    return

        # Time to assign the role! First, I'll remove the user from any current color role they have.
        roles = [a for a in name.roles if not a.name.startswith('clr-')] # This ignores any color role the user has.
        if not role == 'remove': # If they want their color role removed, we skip adding a role because we don't need to. Also it'd cause errors.
            roles.append(role)
        try: # Then, I'll give them the new role.
            await name.edit(roles=roles)
            if not role == 'remove':
                Success('The role\'s been assigned!\n')
                await sendDebug(':white_check_mark: The role\'s been assigned!')
            else:
                Success('Their role\'s been removed!\n')     
                await sendDebug(':white_check_mark: Their role\'s been removed!')
        except:
            Information('Hit an error - chances are, they already have that ' + clr + '. Moving on...\n')
            await sendDebug(':grey_exclamation_mark: Hit an error - chances are, they already have that ' + clr + '. Moving on...')

        Highlight('Checking for unused roles...')
        unused = [a for a in sv.roles if a.name.startswith('clr-') and len(a.members) == 0] # Finally, I'll delete any unused color roles.
        if len(unused) > 0:
            Information('There are ' + str(len(unused)) + ' unused roles.\n')
            await sendDebug(':wastebasket: There are ' + str(len(unused)) + ' unused roles.')
            await setStatus("busy")
            f = 'no'
            c = 0
            while len(unused) > 0:
                try:
                    next = unused[c]
                    await next.delete()
                    Information('I just deleted ' + str(next) + '.\n')
                    await sendDebug('I just deleted `' + str(next) + '`.')
                    c = c + 1
                except discord.errors.NotFound:
                    if f == 'no':
                        f = 1
                    else:
                        f = f + 1
                except IndexError:
                    break
            Success('Okay! I just deleted ' + str(c) + ' unused roles, getting ' + str(f) + ' 404 error(s) due to bad luck!\n')
            await sendDebug(':wastebasket::white_check_mark: Okay! I just deleted ' + str(c) + ' unused roles, getting ' + str(f) + ' 404 error(s) due to bad luck!')
        else:
            Success("There are no unused roles. I'm all done!")
        await setStatus()
        return

## This command will allow a user to move between specific categories and channels, called "floors" and "rooms" respectively.
@bot.command(name='goto',aliases=['move'])
async def goto(ctx, arg1 = '[none]', arg2 = '[none]'):
    Information(str(ctx.message.author) + ' wants to go to ' + str(arg1) + ' "' + str(arg2) + '".\n')
    await sendDebug(':arrow_forward: ' + str(ctx.message.author) + ' wants to go to ' + str(arg1) + ' `' + str(arg2) + '`.')
    if not ctx.guild: # I need to make sure this was sent in the server.
        try: # If not, I won't have any idea what to do, so I'll stop the command here and let them know.
            UserErr(str(ctx.message.author) + ' tried to move, but sent the command in DMs and not in the server.\n')
            await sendDebug(':grey_exclamation: ' + str(ctx.message.author) + ' tried to move, but sent the command in DMs and not in the server. Command halted.\n--')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to move, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can point you in the right direction...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to move from.",f2c="(For reference, your arg2 (the floor/room you want to move *to*) was `" + str(arg2) + "`.)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return

    else: # Otherwise, I'll start the command!
        await setStatus("busy")
        await ctx.message.delete()
        # Defining consistent variables here.
        name = ctx.message.author
        source = ctx.message.channel
        src = str(source)
        dmerror = defaultEmbeds('dmerror', name)
        if arg1 in namedRooms: # If the user just wants to move to a named room, I can autocorrect the command on the fly!
            arg2 = arg1
            arg1 = 'room'
            Information('I just autocorrected the args to make the command work.')

        if arg1 == 'floor': ## For floor movement...
            if arg2 == '[none]': # First, I'll make sure the user didn't forget arg2, and send a DM if they did.
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
            Highlight('Doing some checks...') 
            await sendDebug('Doing some checks...')
            # I need to check to make sure the user is in that floor's lobby.
            sch = str(src.split('-')[0])
            lobby = 'lobby'
            if sch != lobby: # If they aren't in the lobby...
                await sendDebug(':grey_exclamation: The user isn\'t in the lobby. Command halted.\n--')
                UserErr('They weren\'t in the lobby.\n')
                try: # ...I'll send an error in a DM.
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to a different floor, but you're not in the lobby.",f1c="The elevators are in the lobby - not literally, but...you get the point.\n",f2e=1,f2t="**Solution:** Run `" + str(pre) + "goto room lobby` and try again.",f2c="(For reference, you tried to move to floor.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
                await setStatus()
                return

            room = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())] # Otherwise, I'll make sure the floor they request has a lobby.
            if not room: # If the lobby doesn't exist...
                await sendDebug(':grey_exclamation: The floor provided had no lobby. Command halted.\n--')
                try: # ...I'll send an error in a DM.
                    UserErr('There was no lobby for floor ' + str(arg2.lower()) + ', so it probably doesn\'t exist.\n')
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to a different floor, but I couldn't find a lobby for the floor you wanted.",f1c="That typically means the floor doesn't exist.\n",f2e=1,f2t="**Solution:** Check to make sure your floor exists, then run the command again.",f2c="(If you're certain the floor exists, open a ticket in #support.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
                await setStatus()
                return

            if source == room[0]:# Otherwise, I'll check to make sure I'm not wasting time. If it turns out I am...

                await sendDebug(':grey_exclamation: User is already on the floor. Command halted.\n--')
                try: # ...I'll send an error in a DM.
                    UserErr('They tried to move to the same floor.\n')
                    embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to go to the floor you wanted to move to.",f1c="I don't need to guide you if you're already in the right place!~\n",f2e=1,f2t="**Solution:** Check to make sure you didn't mistype the floor number. If you did, fix the typo and run the command again.",f2c="(Check #server-info for more information.)")
                    await name.send(embed=embedVal)
                except discord.Forbidden:
                    await source.send(embed=dmerror)
                await setStatus()
                return
# Otherwise...
# All checks have passed, and I can begin.
            Highlight('Done! Getting ready to move...')
            await sendDebug('Done! Getting ready to move...')
# I'll start by taking the user's permissions for the source floor's #lobby.
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
            await sendDebug('Source perms removed.')
# Then, I'll give the user access to the destination floor's #lobby.
            await room[0].set_permissions(name, overwrite=overwrite)
            Information('Given permissions for ' + str(room[0]) + '...')
            await sendDebug('Target perms given.')
# And I'm finished!
            Success('Floor movement finished!\n')
            await sendDebug('Process complete!\n--')
            await setStatus()
            return

## For room movement...
        elif arg1 in namedRooms:
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
            Highlight('I\'m starting room movement... ')
            await sendDebug('Starting...')
# First, I'll see if arg2 is just a number (i.e., the command run was "goto room 3").
            try:
                newch = int(arg2)
# If it was, I'll append "room" to the beginning of arg2.
                arg2 = str('room' + arg2)
                Information('I just appended "room" to arg2.')
                await sendDebug('Appended "room" to arg2.')
# Otherwise...
            except ValueError:
# ...I can just leave it be.
                pass
# Then, I'll make sure I'm not wasting time.
            destination = str(arg2.lower()) + '-' + str(src.split('-')[1])
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
# Next, I'll check to see if I need to ask for permission to let them in.
            roomName = str(newch[0]).split('-')[0]
            if roomName not in openRooms:
# If I do, I'll see if anybody else is in the room.
                if len(newch[0].members) - len(opIDs) > 0:
# If there are people there, I'll ask for permission.
                    try:
                        host = ctx.guild.get_member(hostIni(1,str(newch[0])))
                        if host == None: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                            await sendDebug(':x: ' + str(opUser) + '**ERROR:** Room host was not found! Command halted.\n--')
                            SysErr('ERROR: I forgot the host of ' + str(newch[0]) + '!! Check "hosts.ini" if it\'s there!\n')
                            embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                            await name.send(embed=embedVal)
                            embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `hosts.ini`.",f1c="See if the [RoomHosts] section is misnamed, or run `tnm!reload` to remake the file and return all stranded users to the lobby.")
                            await opUser.send(embed=embedVal)
                            await setStatus()
                            return

                        # New function to pass a note over to the host!
                        embedVal = generateEmbed(title='The current room host is ' + str(host) + '.',desc='Want me to pass a note to them?')
                        await sendDebug('Asking if the user wants to send a note...')
                        Information('Asking if the user wants to send a note...')
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
                            Information('They want to. Waiting on them...')
                            await sendDebug('They want to. Waiting on them...')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )
                            def check(message: discord.Message):
                                return message.author == name
                            notemsg = await bot.wait_for('message', check=check)
                            noteContents = notemsg.content
                            Information('I got the note! Here\'s the contents:\n"' + str(noteContents) + '"\n"')
                            await sendDebug('I got the note! Here\'s the contents:```' + str(noteContents) + '```')
                            embedVal = generateEmbed(clr=0x33ff00,title='Got it. I\'ll send the request right away!',desc='')
                            await msg.edit(embed=embedVal)
                        else:
                            time = 30
                            sendNote = False
                            Information('They chose not to send a note.')
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
                        Information('I\'ve just asked for permission.')
                        await sendDebug('I\'ve just asked for permission. I\'m now waiting for activity within ' + str(time) + ' seconds...')
                        state = await bot.wait_for('button_click', timeout=time)
                        if state.component.label == "Accept":
                            embedVal = generateEmbed(clr=0x33ff00,title='You granted me permission to add ' + str(name) + ' to ' + str(source) + '.',desc='')
                            await msg.edit(
                                embed=embedVal,
                                components = []
                            )
                            Highlight('Permission was granted by the host.')
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

                elif len(newch[0].members) - len(opIDs) == 0: # Alternatively, if they're the first person to join that room...
                    try: # ...I'll set them as that room's host, then let them know.
                        hostIni(0) # But before I can do that, I'll check to see if hosts.ini exists (and create it if needed).
                        hostIni(2, str(newch[0]), int(name.id))
                        await sendDebug(str(name) + ' was made the host.') # And now I'll let them know!
                        embedVal = generateEmbed(title=":house: **You're the host of " + str(arg2.lower()) + "!**",desc="If somebody tries to join, I'll send you a DM letting you know.\n")
                        await name.send(embed=embedVal)
                    except discord.Forbidden:
                        await source.send(embed=dmerror)
                        await setStatus()
                        return

            roomName = src.split('-')[0] # Now, I'll check the source room's host.
            if len(source.members) - 3 > 0 and (roomName not in openRooms):
                host = hostIni(1, str(source))
                if host == None: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                    await sendDebug(':x: ' + str(opUser) + '**ERROR:** Room host was not found! Command halted.\n--')
                    embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something's gone wrong with my code itself...",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                    await name.send(embed=embedVal)
                    SysErr('Something\'s wrong! I forgot the host of ' + str(source) + '!\n')
                    embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something's gone wrong with my code itself...",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `chost.dat`.",f1c="Check to make sure the file is present, then contact `" + str(name) + "`.")
                    await opUser.send(embed=embedVal)
                    await setStatus()
                    return
                host = ctx.guild.get_member(host)
                if name == host: # If the user is currently the source room's host, and they're leaving...
                    Highlight('The user currently leaving '+ str(roomName) +' is the host. Assigning a new host...')
                    await sendDebug('The user currently leaving '+ str(roomName) +' is the host. Assigning a new host...')
                    sm = []
                    try: # ...I'll add every user that isn't an operator.
                        for m in source.members:
                            if m.id not in opIDs:
                                sm.append(m.id)
                        nhid = int(choice(sm))
                        newhost = ctx.guild.get_member(nhid)
                        Information(str(roomName) + "'s new host is " + str(newhost) + '.')
                        embedVal = generateEmbed(title=":house: **You're now the host of " + str(arg2.lower) + "!**",desc="If somebody tries to join, I'll send you a DM letting you know.\n")
                        await newhost.send(embed=embedVal)
                        hostIni(2,str(source),nhid)
                        await sendDebug('I just made ' + str(newhost) + 'the new host of ' + str(roomName) + '.')
                    except discord.Forbidden:
                        await source.send(embed=dmerror)
                        await setStatus()
                        return
# Otherwise...
# All checks have passed, and I can begin.
            Information('Movement starting...')
# I'll start by taking the user's permissions for the source room...
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
            await sendDebug('Source perms taken.')
# ...and giving them access to the destination room.
            dsf = str(src.split('f')[1])
            await newch[0].set_permissions(name, overwrite=overwrite)
            Information('Given permissions for ' + str(arg2) + '-f' + str(dsf[0]) + '...')
            await sendDebug('Target perms given.')
# And now I'm done!
            Success('Room movement finished!')
            await sendDebug('Process complete!')
# Oh, and if the current host is the last one to leave...
            if len(source.members) - 2 == 0 and (roomName not in openRooms):
# ...I'll recreate the room to clear out the messages.
                await sendDebug('Source is empty. Clearing channel...')
                Highlight('Everyone\'s left, so I\'ll recreate the room to clear its messages...')
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
                embedVal = generateEmbed(title=":grey_question:  **Help: `" + str(pre) + "goto`**",desc="(You're seeing this message because no arguments were provided.)\n",f1e=1,f1t="This command will help me guide you around the Mansion! In order for me to know where you wanna go, you'll need to tell me the following:",f1c="> Whether or not you want to go to a `floor` or a `room`\n> If you want to move to a floor, provide a floor number\n> If you want to move to a room, provide a room name\n",f2e=1,f2t="PLEASE NOTE: If you want to move floors, make sure you're in the lobby before moving!",f2c="Once I have this info, I'll be able to get you to where you need to go!")
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
    if not ctx.guild: # I need to make sure this was sent in the server.
        try: # If not, I won't have any idea what to do, so I'll stop the command here and let them know.
            await sendDebug(':grey_exclamation: Command sent in DMs, so context can\'t be found. Command halted.\n--')
            UserErr(str(ctx.message.author) + ' tried to clear the room, but sent the command in DMs and not in the server.\n')
            await sendDebug('Command was run in DMs. Halted.\n--')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to clear the room you're in, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can figure out what room to clear...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to clear.",f2c="(Maybe one day, I can clear a room from in here. One day...)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return
    else: # Otherwise, I'll start the command!
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
            host = hostIni(1,str(source))
            if host == None: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                await sendDebug(':x: ' + str(opUser) + '**ERROR:** Room host was not found! Command halted.\n--')
                SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this, like, soon!\n')
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                await name.send(embed=embedVal)
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I forgot the host of " + str(source) + ", likely due to a broken or malformed `hosts.ini`.",f1c="Check to make sure the file is present.")
                await opUser.send(embed=embedVal)
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
            Highlight('I\'ve just asked for permission.')
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
        ch = await source.clone()
        await source.edit(name='clearing')
# Once that's done, I'll start moving everyone there.
        await sendDebug('Created a duplicate of ' + str(source) + '. Deleting the original room...')
        Highlight('Created a duplicate of ' + str(source) + '. Deleting the original room...')
        await source.delete()
        await ch.edit(position=pos)
        Success('Room has been cleared.')
        await setStatus()
        return

## This command will close a room, sending everyone back to the lobby and recreating the room.
@bot.command(name='close')
async def close(ctx):
    Information(str(ctx.message.author) + ' just ran: ' + str(pre) + 'close\n')
    await sendDebug(str(ctx.message.author) + ' ran command "clear".')
    if not ctx.guild: # I need to make sure this was sent in the server.
        try: # If not, I won't have any idea what to do, so I'll stop the command here and let them know.
            UserErr(str(ctx.message.author) + ' tried to close the room, but sent the command in DMs and not in the server.\n')
            embedVal = generateEmbed(clr=0xffcc00,title=":warning: **That didn't work...**",desc="An error occurred while processing your command.\n",f1e=1,f1t="**Problem:** You tried to close the room you're in, but sent the command in DMs and not the server.",f1c="I need to know where you are so I can figure out what room to close...\n",f2e=1,f2t="**Solution:** Try running the command again, but in the room you want to close.",f2c="(Maybe one day, I can close a room from in here. One day...)")
            await ctx.send(embed=embedVal)
            return
        except discord.Forbidden:
            return
    else: # Otherwise, I'll start the command!
        await setStatus("busy")
        await ctx.message.delete()
        source = ctx.message.channel
        name = ctx.message.author
        dmerror = defaultEmbeds('dmerror', name)
        roomName = str(source).split('-')[0]
        if (roomName in openRooms): # First, I'll check to make sure the room isn't an open room. If so...
            UserErr('This is an open room...\n')
            await ctx.send('This is an open room...')
            await setStatus()
            return
        try: # Otherwise, I'll make sure the host wants to close the room...
            host = hostIni(1,str(source))
            if host == None: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                await sendDebug(':x: ' + str(opUser) + '**ERROR:** I couldn\'t find a `chost.dat` file! Command halted.\n--')
                SysErr('Oh CRAP!! I couldn\'t find a `chost.dat` file!\n')
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I can't remember the host of " + str(source) + ".",f1c="I've just contacted the system operator - they'll follow up with you once the issue is fixed.")
                await name.send(embed=embedVal)
                embedVal = generateEmbed(clr=0xff0000,title=":x:  **I've encountered a fatal error!**",desc="Something has gone wrong with my code itself.",f1e=1,f1t="**Problem:** I can't remember the host of " + str(source) + ", likely due to a broken, malformed, or non-existent `chost.dat`.",f1c="Check to make sure the file is present.")
                await opUser.send(embed=embedVal)
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
            Information('I\'ve just asked for permission.')
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
        ch = 'lobby-' + str(ctx.message.channel).split('-')[1]
        ch = [a for a in bot.get_all_channels() if a.name == str(ch)]
        sm = []
        for m in source.members: # ...I'll add every user that isn't an operator.
            if m.id not in opIDs:
                sm.append(m.id)
        for u in sm:
            await source.set_permissions(u, overwrite=None)
            await ch[0].set_permissions(u, overwrite=overwrite)
            await sendDebug('Moved user ' + str(u) + '.')
        Information('All users have been moved back to the lobby. Recreating the room...')
        await sendDebug('All users have been moved back to the lobby. Recreating the room...')
        pos = int(source.position) # Now, I'll recreate the room to clear out the messages.
        cch = await source.clone()
        await source.delete()
        await cch.edit(position=pos)
        Success('Room has been closed.')
        await sendDebug('Room closed.\n--')
        await setStatus()
        return


## OTHER COMMANDS ##
## This command allows the user to view the Boost Software License.
@bot.command(name='license',aliases=['bsl'])
async def license(ctx):
    if ctx.guild:
        await ctx.message.delete()
    embedVal = discord.Embed(title=':page_facing_up: **Boost Software License**', description='TNM-chan is licensed under the Boost Software License, which gives you specific rights to the source code. Click the button below to view the License in your browser.')
    components = [
    [
        Button(style=ButtonStyle.URL, label="View in Browser", url='https://github.com/heyitzrare/tnm-chan/blob/master/LICENSE.TXT')
    ]
            ]
    try:
        await ctx.message.author.send(embed=embedVal, components=components)
    except discord.Forbidden:
        embedVal.add_field(
            name='***Please* enable DMs from server members...**',
            value="I'd prefer to send stuff like this in DMs, as to not create unnecessary clutter in the server. That said, could you enable DMs from server members, please? It'd make me happy!"
        )
        try:
            await ctx.message.channel.send(embed=embedVal)
        except:
            return

## Here's a command list. Remember, more details are given when the commands are run.
@bot.command(name='help', aliases=['list'])
async def list(ctx):
    Information(str(ctx.message.author) + ' just requested the command list.\n')
    if ctx.guild:
        await ctx.message.delete()
    embedVal = discord.Embed(color=0x03FFED, title=':grey_question:  **Command List**',
    description='Prefix your command with `' + str(pre) + '` to run the command. Commands may be added, altered, or removed in the future.\n--')

    embedVal.add_field(name='Core Commands',
    value='**Note:** To get help, run the command without arguments.\n> **' + clr + ':** Creates a unique ' + clr + ' role for your name. (Both forms of the word will work, so don\'t worry about that being an issue!)\n> **goto/move:** Move between floors/rooms.', inline=False)
    
    embedVal.add_field(name='Room Commands',
    value='**Note:** You *must* be the room host to use these commands.\n> **clear:** Deletes all messages in a room without moving members.\n> **close:** Deletes all messages in a room and moves all members back to the lobby.', inline=False)
    
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

## This command will send the user a link to my source code.
@bot.command(name='source',aliases=['github','code','sourcecode'])
async def source(ctx):
    if ctx.guild:
        await ctx.message.delete()
    embedVal = generateEmbed(title=":desktop: You can find my source code here!",desc="https://github.com/heyitzrare/tnm-chan")
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


## ADMIN COMMANDS ## (These are only supposed to be run by an admin - ordinary members won't be able to run these!)
## This command reloads my settings and colorset. Use it if you've made changes!
@bot.command(name='refresh',aliases=['reload', 'reset'])
async def refresh(ctx, x=False):
    if ctx.guild:
        await ctx.message.delete()
    auth = ctx.message.author
    if auth.id == opUser.id:
        if x:
            m = await auth.send('Resetting settings, colorset, and hosts.ini...')
            hostIni(0,True)
        else:
            m = await auth.send('Resetting settings/colorset and checking if hosts.ini exists...')
            hostIni(0)
        refreshSettings()
        reloadColorSet()
        await m.edit('Done!')
    else:
        UserErr(str(auth) + " tried to reset internal settings, but they aren't an admin!")
        return

bot.run(TOKEN) # I think this has to be *here,* for some reason...oh well!~