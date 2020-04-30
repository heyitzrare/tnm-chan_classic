### TNM-chan ###
## v20.118-r1 ##

# I'm getting started! First, I'll import/load libraries and stuff.
import traceback
import os
import sys
import pickle
import time
import asyncio
from random import choice
try: color = sys.stdout.shell
except AttributeError: raise RuntimeError("Use IDLE")
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Now, this token is used to get in to Discord's APIs.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# I'm setting my command prefix. In this case, it's 'tnm!'.
bot = commands.Bot(command_prefix='tnm!')

# Now, I'll set up constant variables here.
overwrite = discord.PermissionOverwrite()
overwrite.send_messages=True
overwrite.read_messages=True

dmWelcome = '> **Hi there, and welcome to The Neptunia Mansion!**\nI\'m TNM-chan, your android assistant. If you\'d like to go somewhere, call me with the following command:\n```tnm!goto floor|room [floor number]|[room name]```\nI\'ll handle the rest! And if I ever go offline, let my creator know! His Discord name is:\n`HeyItzRare#0987`'

# If all went well, I'll send a message to the terminal!
@bot.event
async def on_ready():
    color.write('Connected.\n', 'STRING')

# Here's how I welcome new users, and add them to #lobby-f1!
@bot.event
async def on_member_join(ctx):
    member = ctx
    color.write('Hey! ' + str(ctx) + ' just joined the server.\n', 'DEFINITION')
    channel = [a for a in bot.get_all_channels() if a.name == 'lobby-f1']
    await channel[0].set_permissions(member, overwrite=overwrite)
    color.write('They now have access to #lobby-f1...', 'COMMAND')
    try:
        await member.send(dmWelcome)
        color.write('and the welcome DM\'s been sent. ', 'COMMAND')
    except discord.Forbidden:
        dmErrorFirst = 'Hi there, ' + str(ctx.mention) + '! To get the most out of the server, you\'ll need to turn on DMs from server members. Otherwise, you won\'t be able to host channels or see error messages. I promise, we won\'t spam you!'
        await channel[0].send(dmErrorFirst)
        color.write('and I\'ve asked them to enable DMs from server members. Try to make sure they actually do this... ', 'KEYWORD')
    color.write('All set!\n\n', 'STRING')
    
# Okay, here's my commands!

# Here's my super special command for channel/category movement~
@bot.command(name='goto')
async def goto(ctx, arg1 = 'fail', arg2 = 'fail'):
    color.write(str(ctx.message.author) + ' just ran: tnm!goto ' + str(arg1) + ' ' + str(arg2) + '\n', 'COMMAND')
    await ctx.message.delete()
# Defining consistent variables here.
    name = ctx.message.author
    source = ctx.message.channel
    src = str(source)
    dmError = 'Hi, ' + str(name.mention) + '! I tried to send you a DM, but it seems you\'ve disabled the option to allow DMs from server members. You\'ll need to turn that on to host channels and receive error messages from the server.'
    sourcecat = source.category
## For floor movement...
    if arg1 == 'floor':
# First, I'll make sure the user didn't forget arg2, and send a DM if they did.
        if arg2 == 'fail':
            try:
                await name.send('**Remember:** You need to tell me *which* floor you want to move to.')
                color.write('Confusion... ' + str(name) + ' tried to move, but didn\'t say which floor to move to.\n\n', 'KEYWORD')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return
# Then, I'll let the terminal know I'm starting.
        destination = arg2.lower()
        color.write('I\'m starting floor movement... ', 'DEFINITION')
        color.write(str(name) + ' is trying to move from ' + str(sourcecat) + ' to Floor ' + str(destination) + '.\n', 'COMMAND')
# Next, I'll check to make sure the user is in that floor's lobby.
        sch = str(src.split('-')[0])
        lobby = 'lobby'
# If they aren't in the lobby...
        if sch != lobby:
# ...I'll send an error in a DM.
            try:
                await name.send('**Sorry, but...** You can\'t move floors outside of the lobby.\nTry running `tnm!goto room lobby` first.')
                color.write('Whoops! They weren\'t in the lobby.\n\n', 'KEYWORD')
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
                color.write('Whoops! There was no lobby for floor ' + str(arg2.lower()) + '.\n\n', 'KEYWORD')
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
                color.write('Silly... They tried to move to the same floor.\n\n', 'KEYWORD')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source floor's #lobby.
        await source.set_permissions(name, overwrite=None)
        color.write('Taken permissions for ' + str(source) + '...\n', 'COMMAND')
# Then, I'll send a message in the source channel, stating the user has left.
        response = str(name.mention) + ' has left the room.'
        await source.send(response)
# Next, I'll send a message to the destination channel, stating the user has joined.
        response = str(name.mention) + ' has entered the room.'
        target = 'lobby-f' + str(arg2.lower())
        destination = [a for a in bot.get_all_channels() if a.name == str(target)]
        await destination[0].send(response)
# Lastly, I'll give the user access to the destination floor's #lobby.
        channel = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())]
        channel = channel[0]
        await channel.set_permissions(name, overwrite=overwrite)
        color.write('Given permissions for ' + str(channel) + '...\n', 'COMMAND')
# And I'm finished!
        color.write('Floor movement finished!\n\n', 'STRING')
        return

## For room movement...
    elif arg1 == 'room':
# I need to make sure the user didn't forget arg2, and send a DM if they did.
        if arg2 == 'fail':
            try:
                await name.send('**Remember:** You need to tell me *which* room you want to move to!')
                color.write('Confusion... ' + str(name) + ' tried to move, but didn\'t say which room to move to.\n\n', 'KEYWORD')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return
# I'll let the terminal know before starting.
        destination = arg2.lower()
        color.write('I\'m starting room movement... ', 'DEFINITION')
        color.write(str(name) + ' is trying to move from ' + str(source) + ' to ' + str(destination) + '\n', 'COMMAND')
# First, I'll make sure I'm not wasting time.
        destination = str(arg2.lower()) + '-' + str(src.split('-')[1])
# If it turns out I am...
        if src == destination:
# ...I'll send an error message in a DM.
            try:
                await name.send('Hey, I don\'t move you if you\'re already in the right room~')
                color.write('Silly... They tried to move to the same room.\n\n', 'KEYWORD')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return
# OItherwise...
# Then, I'll make sure the room exists.
        newch = [a for a in bot.get_all_channels() if a.name == str(destination)]
# And if it doesn't...
        if not newch:
# ...I'll send an error in a DM.
            try:
                await name.send('**Sorry, but...** The room you requested doesn\'t exist.')
                color.write('Whoops! They tried to move to a channel that doesn\'t exist.\n\n', 'KEYWORD')
                return
            except discord.Forbidden:
                await source.send(dmError)
                return
# Otherwise...
# Next, I'll check to see if I need to ask for permission to let them in.
        test = (str(arg2.lower()) == 'lobby' or str(arg2.lower()) == 'entroom')
        if test == False:
# If I do, I'll see if anybody else is in the channel.
            if len(newch[0].members) - 2 > 0:
# If there are people there, I'll ask for permission.
                try:
                    try:
                        with open('chost.tnmc', 'rb+') as f:
                            host = pickle.load(f)[str(newch[0]) + '-host']
                    except KeyError:
                        await name.send('**Eep!** Sorry, I think I forgot the host of `#' + str(newch[0]) + '`... Could you let `HeyItzRare#0987` know? He\'ll be able to fix it!')
                        color.write('AHH!! I forgot the host of ' + str(newch[0]) + '!! Please fix this, like, soon!\n\n', 'COMMENT')
                        return
                    host = ctx.guild.get_member(host)
                    reactm = await host.send(str(name) + ' wants to join ' + str(source) + '. You must react within 10 seconds to accept.')
                    await reactm.add_reaction('☑')
                    def check(reaction, user):
                        return reaction.count > 1 and reaction.message.id == reactm.id and str(reaction.emoji) == '☑'
                    color.write('I\'ve just asked for permission...', 'DEFINITION')
                    reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
                    await reactm.edit(content='Permission was granted.')
                    color.write('and permission was granted by the host. Continuing!\n', 'STRING')
                except asyncio.TimeoutError:
                    try:
                        await reactm.edit(content='Permission was automatically denied.')
                        await name.send('Unfortunately, a channel member didn\'t let you in...')
                        color.write('no reaction from the host, so permission was automatically denied.\n\n', 'KEYWORD')
                        return
                    except discord.Forbidden:
                        await source.send(dmError)
                        return
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Or, if they're the first person to join that channel...
            elif len(newch[0].members) - 2 == 0:
# ...I'll set them as that channel's host, and let them know.
                try:
                    with open('chost.tnmc', 'rb+') as f:
                        chost = {}
                        newid = int(name.id)
                        pickle.dump({str(newch[0]) + '-host': int(newid)}, f)
                    await name.send('**Hi!** Since you\'re the first person to join the room, you\'re its host. If anyone else tries to join, I\'ll ask you.')
                    color.write('I just made ' + str(name) + ' the room host.\n', 'DEFINITION')
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# If the user is currently the room host...
        test = str(src.split('-')[0]) == 'lobby' or str(src.split('-')[0]) == 'entroom'
        if len(source.members) - 2 > 0 and test == False:
            try:
                with open('chost.tnmc', 'rb+') as f:
                    host = pickle.load(f)[str(source) + '-host']
            except KeyError:
                await name.send('**Eep!** Sorry, I think I forgot the host of `#' + str(source) + '`... Could you let `HeyItzRare#0987` know? He\'ll be able to fix it!')
                color.write('AHH!! I forgot the host of ' + str(source) + '!! Please fix this, like, soon!\n\n', 'COMMENT')
                return
            host = ctx.guild.get_member(host)
            if name == host:
# ...I'll assign another random member to be the new host of the room.
                try:
                    newhost = choice(source.members)
                    nhid = int(newhost.id)
                    counter = 1
                    while  nhid == [number]: # Replace this so I don't accidentally make myself - or you - the server host.
                        newhost = choice(source.members)
                        nhid = int(newhost.id)
                        counter = counter + 1
                    with open('chost.tnmc', 'rb+') as f:
                        chost = {}
                        pickle.dump({str(source) + '-host': int(nhid)}, f)
                    host = ctx.guild.get_member(host)
                    await newhost.send('**Hi!** Since the previous host just left ' + str(source) + ', you\'re its new host now. If anyone else tries to join, I\'ll ask you.')
                    color.write(str(name) + ' just left, so I made ' + str(newhost) + 'the new room host. It took ' + str(counter) + ' tries to find a new host.\n', 'DEFINITION')
                except discord.Forbidden:
                    await source.send(dmError)
                    return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source channel.
        await source.set_permissions(name, overwrite=None)
        color.write('Taken permissions for ' + str(source) + '...\n', 'COMMAND')
# Then, I'll send a message in the source channel, stating the user has left.
        response = str(name.mention) + ' has left the room.'
        await source.send(response)
# Next, I'll send a message to the destination channel, stating the user has joined.
        response = str(name.mention) + ' has entered the room.'
        await newch[0].send(response)
# Finally, I'll give the user access to the destination channel.
        await newch[0].set_permissions(name, overwrite=overwrite)
        color.write('Given permissions for lobby-f' + str(destination[0]) + '...\n', 'COMMAND')
# And now I'm done!
        color.write('And they\'ve been moved to the new room!\n\n', 'STRING')

## But...maybe they forgot arg1.
    elif arg1 == 'fail':
        try:
            await name.send('**Remember:** You need to type the following:\n```tnm!goto floor|room [floor number]|[room name]```')
            color.write('Confusion... ' + str(name) + ' tried to move, but didn\'t provide an arg1.\n\n', 'KEYWORD')
            return
        except discord.Forbidden:
            await source.send(dmError)
            return
# Or, if they mistyped...
    else:
        try:
            await name.send('**Sorry, but...** I can only understand `floor` or `room` for the first argument. You said `' + str(arg1) + '`.')
            color.write('Confusion... ' + str(name) + ' tried to move, but provided an invalid arg1. They tried to use `' + str(arg1) + '" .\n\n', 'KEYWORD')
            return
        except discord.Forbidden:
            await source.send(dmError)
            return
bot.run(TOKEN)
