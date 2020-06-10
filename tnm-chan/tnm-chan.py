### TNM-chan ###
### v 20.162 ###

###IMPORTANT!###
# Put your Discord username in between the quotes - make sure this is right, because I send it if something goes wrong!
sysop = ""

# Before launching the bot, take note of any moderators (including me) that have access to all channels, and copy their IDs into this list. 
opIDs = [
    
]

### --- ###
## I'm getting started!

# First, I'll import/load libraries.
import traceback
import os
import sys
import shelve
import time
import asyncio
from random import choice
from termcolor import colored, cprint
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Now, the token specified in the .env is used to get in to Discord's APIs.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# I'm setting my command prefix. In this case, it's 'tnm!'.
bot = commands.Bot(command_prefix='tnm!')

# I'm defining my new, cross-platform color writing.
def Information(skk): print("\033[97m {}\033[00m" .format(skk)) # Gray

def Success(skk): print("\033[92m {}\033[00m" .format(skk)) # Green

def UserErr(skk): print("\033[93m {}\033[00m" .format(skk)) # Yellow
def SysErr(skk): print("\033[91m {}\033[00m" .format(skk)) # Red

def Permission(skk): print("\033[95m {}\033[00m" .format(skk)) # Purple
def Intent(skk): print("\033[34m {}\033[00m" .format(skk)) # Blue
def Conversion(skk): print("\033[96m {}\033[00m" .format(skk)) # Cyan

# Now, I'll set up constant variables here.
firstConnect = True

overwrite = discord.PermissionOverwrite()
overwrite.send_messages=True
overwrite.read_messages=True

dmWelcome = '> **Hi there, and welcome to The Neptunia Mansion!**\nI\'m TNM-chan, your android assistant. If you\'d like to go somewhere, call me with the following command:\n```tnm!goto floor|room [floor number]|[room name]```\nI\'ll handle the rest! By the way, I ever go offline, let my operator know! Their Discord name is:\n`' + str(sysop) + '`'

# If all went well, I'll send a message to the terminal!
@bot.event
async def on_ready():
    global firstConnect
    if firstConnect:
        firstConnect = False
        Intent('I\'ve connected to the server!\n')
    else:
        Intent('I got disconnected, but I\'m back online!\n')
# Here's how I welcome new users, and add them to the main channel!
@bot.event
async def on_member_join(ctx):
    member = ctx
    Intent('Hey! ' + str(ctx) + ' just joined the server.')
    channel = [a for a in bot.get_all_channels() if a.name == 'lobby-f1']
    await channel[0].set_permissions(member, overwrite=overwrite)
    Information('They now have access to #lobby-f1.')
    try:
        await member.send(dmWelcome)
        Information('The welcome DM\'s been sent. ')
    except discord.Forbidden:
        dmErrorFirst = 'Hi there, ' + str(ctx.mention) + '! To get the most out of the server, you\'ll need to turn on DMs from server members - at least, from *this* server. Otherwise, you won\'t be able to host channels or see important information. I promise, we won\'t spam you!'
        await channel[0].send(dmErrorFirst)
        UserErr('I\'ve asked them to enable DMs from server members. Try to make sure they actually do this... ')
    Success('All set!\n')
    
### Okay, here's my commands!

## Here's my super special command for channel/category movement! Trey, make sure you get it right this time!
@bot.command(name='goto')
async def goto(ctx, arg1 = '[none]', arg2 = '[none]'):
    Information(str(ctx.message.author) + ' just ran: tnm!goto ' + str(arg1) + ' ' + str(arg2) + '\n')
# I need to make sure this was sent in the server.
    if not ctx.guild:
# If not, I won't have any idea what to do, so I'll stop the command here and let them know.
        try:
            await ctx.message.author.send('**Hey, wait!** You need to run this in the server, otherwise I\'ll get confused....')
            UserErr('Whoops! ' + str(ctx.message.author) + ' tried to move, but sent the command in DMs and not in the server.\n')
            return
        except discord.Forbidden:
            return
# Otherwise, I'll start the command!
    else:
        await ctx.message.delete()
# Defining consistent variables here.
        name = ctx.message.author
        source = ctx.message.channel
        src = str(source)
        dmError = 'Hi, ' + str(name.mention) + '! I tried to send you a DM, but it seems you\'ve disabled the option to allow DMs from server members. You\'ll need to turn that on to host channels and receive important information from the server.'

## For floor movement...
        if arg1 == 'floor':
            sourcecat = source.category
# First, I'll make sure the user didn't forget arg2, and send a DM if they did.
            if arg2 == '[none]':
                try:
                    await name.send('**Remember:** You need to tell me *which* floor you want to move to.')
                    UserErr('Confusion... ' + str(name) + ' tried to move, but didn\'t say which floor to move to.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Then, I'll let the terminal know I'm starting.
            destination = arg2.lower()
            Intent('I\'m starting floor movement... ')
            Information(str(name) + ' is trying to move from ' + str(sourcecat) + ' to Floor ' + str(destination) + '.')
# Next, I'll check to make sure the user is in that floor's lobby.
            sch = str(src.split('-')[0])
            lobby = 'lobby'
# If they aren't in the lobby...
            if sch != lobby:
# ...I'll send an error in a DM.
                try:
                    await name.send('**Sorry, but...** You can\'t move floors outside of the lobby.\nTry running `tnm!goto room lobby` first.')
                    UserErr('Whoops! They weren\'t in the lobby.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Otherwise...
# Next, I'll make sure the floor they request has a lobby.
            channel = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())]
# If the lobby doesn't exist...
            if not channel:
# ...I'll send an error in a DM.
                try:
                    await name.send('**Sorry, but...** The floor you requested doesn\'t have a lobby.')
                    UserErr('Whoops! There was no lobby for floor ' + str(arg2.lower()) + '.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Otherwise...
# Finally, I'll check to make sure I'm not wasting time.
# If it turns out I am...
            if source == channel[0]:
# ...I'll send an error in a DM.
                try:
                    await name.send('Hey, I don\'t need to move you if you\'re already on the right floor~')
                    UserErr('Silly... They tried to move to the same floor.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source floor's #lobby.
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
# Then, I'll send a message in the source channel, stating the user has left.
            response = str(name.mention) + ' has left the room.'
            await source.send(response)
# Next, I'll send a message to the destination channel, stating the user has joined.
            response = str(name.mention) + ' has entered the room.'
            target = 'lobby-f' + str(arg2.lower())
            destination = [a for a in bot.get_all_channels() if a.name == str(target)]
            await destination[0].send(response)
# Lastly, I'll give the user access to the destination floor's #lobby.
            await destination[0].set_permissions(name, overwrite=overwrite)
            Information('Given permissions for ' + str(destination[0]) + '...')
# And I'm finished!
            Success('Floor movement finished!\n')
            return

## For room movement...
        elif arg1 == 'room':
# I need to make sure the user didn't forget arg2, and send a DM if they did.
            if arg2 == '[none]':
                try:
                    await name.send('**Remember:** You need to tell me *which* room you want to move to!')
                    UserErr('Confusion... ' + str(name) + ' tried to move, but didn\'t say which room to move to.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# I'll let the terminal know before starting.
            dest = arg2.lower()
            Intent('I\'m starting room movement... ')
            Information(str(name) + ' is trying to move from ' + str(source) + ' to ' + str(dest) + '\n')
# First, I'll see if arg2 is just a number (i.e., the command run was "tnm!goto room 3").
            try:
                newch = int(arg2)
# If it was, I'll append "room" to the beginning of arg2.
                Conversion('I\'ll convert this...')
                convert = str('room' + arg2)
                Conversion('...and done!')
# Otherwise...
            except ValueError:
                convert = str(arg2)
                Conversion('No need to convert!')
# Then, I'll make sure I'm not wasting time.
            destination = str(convert.lower()) + '-' + str(src.split('-')[1])
# If it turns out I am...
            if src == destination:
# ...I'll send an error message in a DM.
                try:
                    await name.send('Hey, I don\'t move you if you\'re already in the right room~')
                    UserErr('Silly... They tried to move to the same room.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Otherwise...
# Next, I'll make sure the room exists.
            newch = [a for a in bot.get_all_channels() if a.name == str(destination)]
# And if it doesn't...
            if not newch:
# ...I'll send an error in a DM.
                try:
                    await name.send('**Sorry, but...** The room you requested doesn\'t exist.')
                    UserErr('Whoops! They tried to move to a channel that doesn\'t exist.\n')
                    return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Otherwise...
# Next, I'll check to see if I need to ask for permission to let them in.
            test = (str(arg2.lower()) == 'lobby' or str(arg2.lower()) == 'entroom') # The lobby and entroom are open rooms.
            if not test:
# If I do, I'll see if anybody else is in the channel.
                if len(newch[0].members) - 2 > 0:
# If there are people there, I'll ask for permission.
                    try:
                        try:
                            with shelve.open('chost') as f:
                                host = f[str(newch[0]) + '-host']
                        except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                            await name.send('**Eep!** Sorry, I forgot the host of `#' + str(newch[0]) + '`... Could you let `' + str(sysop) + '` know? He\'ll be able to fix it!')
                            SysErr('AHH!! I forgot the host of ' + str(newch[0]) + '!! Please fix this, like, soon!\n')
                            return
                        host = ctx.guild.get_member(host)
                        reactm = await host.send(str(name) + ' wants to join ' + str(source) + '. You must react within 10 seconds to accept.')
                        await reactm.add_reaction('☑')
                        def check(reaction, user):
                            return reaction.count > 1 and reaction.message.id == reactm.id and str(reaction.emoji) == '☑'
                        Permission('I\'ve just asked for permission...')
                        await bot.wait_for('reaction_add', timeout=10, check=check)
                        await reactm.edit(content='Permission was granted.')
                        Success('Permission was granted by the host.')
                    except asyncio.TimeoutError: # If the room host doesn't react in time, I'll do this:
                        try:
                            await reactm.edit(content='Permission was automatically denied.')
                            await name.send('Unfortunately, a channel member didn\'t let you in...')
                            UserErr('No reaction from the host, so permission was automatically denied.\n')
                            return
                        except discord.Forbidden:
                            await source.send(dmError)
                            return
                    except discord.Forbidden:
                        await source.send(dmError)
                        return
# Or, if they're the first person to join that channel...
                elif len(newch[0].members) - 2 == 0:
# ...I'll set them as that channel's host, then let them know.
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
# After checking, I'll set the user as the host.
                        with shelve.open('chost') as f:
                                chost = {}
                                newid = int(name.id)
                                f[str(newch[0]) + '-host'] = int(newid)
                        await name.send('**Hi!** Since you\'re the first person to join the room, you\'re its host. If anyone else tries to join, I\'ll ask you.')
                        Intent('I just made ' + str(name) + ' the room host.')
                    except discord.Forbidden:
                        await source.send(dmError)
                        return
# If the user is currently the room host...
            test = str(src.split('-')[0]) == 'lobby' or str(src.split('-')[0]) == 'entroom'
            if len(source.members) - 2 > 0 and not test:
                try:
                    with shelve.open('chost') as f:
                        host = f[str(source) + '-host']
                except KeyError: # In the EXTREMELY rare event I forget the host of the room, I'll do this:
                    await name.send('**Eep!** Sorry, I think I forgot the host of `#' + str(source) + '`... Could you let `' + str(sysop) + '` know? He\'ll be able to fix it!')
                    SysErr('AHH!! I forgot the host of ' + str(source) + '!! Please fix this!\n')
                    return
                host = ctx.guild.get_member(host)
                if name == host:
# ...I'll assign another random member to be the new host of the room.
                    try:
                        newhost = choice(source.members)
                        nhid = int(newhost.id)
                        counter = 1
                        while nhid in opIDs: # This is so I don't accidentally make myself or admin the room host.
                            newhost = choice(source.members)
                            nhid = int(newhost.id)
                            counter = counter + 1
                        with shelve.open('chost') as f:
                            chost = {}
                            f[str(source) + '-host'] = int(nhid)
                        nhost = ctx.guild.get_member(newhost)
                        await nhost.send('**Hi!** Since the previous host just left ' + str(source) + ', you\'re its new host now. If anyone else tries to join, I\'ll ask you.')
                        Intent(str(name) + ' just left, so I made ' + str(newhost) + 'the new room host. It took ' + str(counter) + ' tries to find a new host.')
                    except discord.Forbidden:
                        await source.send(dmError)
                        return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source channel.
            await source.set_permissions(name, overwrite=None)
            Information('Taken permissions for ' + str(source) + '...')
# Then, I'll send a message in the source channel, stating the user has left.
            response = str(name.mention) + ' has left the room.'
            await source.send(response)
# Oh, and if the current host is the last one to leave...
            if len(source.members) - 2 == 0 and not test:
# ...I'll recreate the channel to clear out the messages.
                Intent('Everyone\'s left, so I\'ll recreate the channel to clear its messages...')
                pos = int(source.position)
                cch = await source.clone()
                await source.delete()
                await cch.edit(position=pos)
                Success('Alright, done! Continuing...')
# Next, I'll send a message to the destination channel, stating the user has joined.
            response = str(name.mention) + ' has entered the room.'
            await newch[0].send(response)
# Finally, I'll give the user access to the destination channel.
            dsf = str(src.split('f')[1])
            await newch[0].set_permissions(name, overwrite=overwrite)
            Information('Given permissions for ' + str(convert) + '-f' + str(dsf[0]) + '...')
# And now I'm done!
            Success('Room movement finished!\n')

# Oh, and if the current host is the last one to leave...
            if len(source.members) - 2 == 0 and not test:
# ...I'll recreate the channel to clear out the messages.
                Information('Everyone\'s left, so I\'ll recreate the channel to clear its messages...')
                pos = int(source.position)
                cch = await source.clone()
                await source.delete()
                await cch.edit(position=pos)
                Success('Alright, done!\n')

## In case they forgot arg1...
        elif arg1 == '[none]':
            try:
                await name.send('**Remember:** You need to type the following:\n```tnm!goto floor|room [floor number]|[room name]```')
                UserErr('Confusion... ' + str(name) + ' tried to move, but didn\'t provide an arg1.\n')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return
# Or, if they mistyped arg1...
        else:
            try:
                await name.send('**Sorry, but...** I can only understand `floor` or `room` for the first argument. You said `' + str(arg1) + '`.')
                UserErr('Confusion... ' + str(name) + ' tried to move, but provided an invalid arg1. They tried to use `' + str(arg1) + '" .\n')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return

bot.run(TOKEN)
