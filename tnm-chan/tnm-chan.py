### TNM-chan ###

# I'm getting started! First, I'll import/load libraries and stuff.
import traceback
import os
import sys
import time
import asyncio
try: color = sys.stdout.shell
except AttributeError: raise RuntimeError("Use IDLE")
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Now, this token is used to get in to Discord's APIs.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# I'm setting my command prefix, "tnm!"
bot = commands.Bot(command_prefix='tnm!')

# If all went well, I'll send a message to the terminal!
@bot.event
async def on_ready():
    color.write('Connected.\n', 'STRING')

# Here's how I welcome new users, and add them to #lobby-f1!
@bot.event
async def on_member_join(ctx):
    member = ctx
    color.write('TNM-chan here! ' + str(ctx) + ' just joined! Initiating Welcome!\n', 'DEFINITION')
    channel = [a for a in bot.get_all_channels() if a.id == 701835579066679418][0]
    await channel.set_permissions(member, read_messages=True,
                                                        send_messages=True)
    color.write('They now have access to #lobby-f1...', 'DEFINITION')
    await member.send('> **Hi there, and welcome to The Neptunia Mansion!**\nI\'m TNM-chan, your android assistant. If you\'d like to go somewhere, call me with the following command:\n```tnm!goto floor|room [floor number]|[room name]```\nI\'ll handle the rest! And if I ever go offline, let my creator know! His Discord name is:\n`HeyItzRare#0987`')
    color.write('and I\'ve DMed them! Welcome complete~\n', 'DEFINITION')
# Okay, here's my commands!

# Here's my super special command for channel/category movement~
@bot.command(name='goto')
async def goto(ctx, arg1 = 'fail', arg2 = 'fail'):
    await ctx.message.delete()
## For floor movement...
    if arg1 == 'floor':
# First, I'll make sure the user didn't forget arg2, and send a DM if they did.
        if arg2 == 'fail':
            await ctx.message.author.send('**Remember:** You need to tell me *which* floor you want to move to!')
            color.write('Confusion... ' + str(ctx.message.author) + ' tried to move, but didn\'t say which floor to move to.\n', 'COMMENT')
            return
# Then, I'll let the terminal know before starting.
        name = ctx.message.author
        source = ctx.message.channel.category
        destination = arg2.lower()
        color.write('I\'m starting floor movement... ', 'DEFINITION')
        color.write(str(name) + ' is trying to move from ' + str(source) + ' to floor ' + str(destination) + '.\n', 'COMMAND')
# Next, I'll check to make sure the user is in that floor's lobby.
        sch = str(ctx.message.channel)
        source = str(sch.split('-')[0])
        lobby = 'lobby'
# If they aren't in the lobby...
        if source != lobby:
# ...I'll send an error in a DM.
            await ctx.message.author.send('**Sorry, but...** You can\'t move floors outside of the lobby.\nTry running `tnm!goto room lobby` first.')
            color.write('Whoops! They weren\'t in the lobby.\n', 'COMMENT')
            return
# Otherwise...
# Next, I'll make sure the floor they request has a lobby.
        channel = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())]
# If the lobby doesn't exist...
        if not channel:
# ...I'll send an error in a DM.
            await ctx.message.author.send('**Sorry, but...** The floor you requested doesn\'t have a lobby.')
            color.write('Whoops! There was no lobby for floor ' + str(arg2.lower()) + '.\n', 'COMMENT')
            return
# Otherwise...
# Finally, I'll check to make sure I'm not wasting time.
        source = ctx.message.channel
        destination = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())]
# If it turns out I am...
        if source == destination[0]:
# ...I'll send an error in a DM.
            await ctx.message.author.send('Hey, I don\'t need to move you if you\'re already on the right floor~')
            color.write('Silly... They tried to move to the same floor.\n', 'KEYWORD')
            return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source floor's #lobby.
        source = ctx.message.channel
        await ctx.message.channel.set_permissions(ctx.message.author, overwrite=None)
        color.write('Taken permissions for ' + str(source) + '...\n', 'COMMAND')
# Lastly, I'll give the user access to the destination floor's #lobby.
        channel = [a for a in bot.get_all_channels() if a.name == 'lobby-f' + str(arg2.lower())]
        channel = channel[0]
        member = ctx.message.author
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages=True
        overwrite.read_messages=True
        await channel.set_permissions(member, overwrite=overwrite)
        color.write('Given permissions for ' + str(channel) + '...\n', 'COMMAND')
# And I'm finished!
        color.write('And the movement\'s done!\n', 'STRING')
        return

## For room movement...
    elif arg1 == 'room':
# I need to make sure the user didn't forget arg2, and send a DM if they did.
        if arg2 == 'fail':
            await ctx.message.author.send('**Remember:** You need to tell me *which* room you want to move to!')
            color.write('Confusion... ' + str(ctx.message.author) + ' tried to move, but didn\'t say which room to move to.\n', 'COMMENT')
            return
# I'll let the terminal know before starting.
        name = ctx.message.author
        source = ctx.message.channel
        destination = arg2.lower()
        num = ctx.message.channel.category
        color.write('Starting room movement... ', 'DEFINITION')
        color.write(str(name) + ' from ' + str(source) + ' to ' + str(destination) + ' on ' + str(num) + '\n', 'COMMAND')
# First, I'll make sure I'm not wasting time.
        source = str(ctx.message.channel)
        destination = str(arg2.lower()) + '-' + str(source.split('-')[1])
# If it turns out I am...
        if source == destination:
# ...I'll send an error message in a DM.
            await ctx.message.author.send('Hey, I don\'t move you if you\'re already in the right room~')
            color.write('Silly... They tried to move to the same room.\n', 'KEYWORD')
            return
# OItherwise...
# Then, I'll make sure the room exists.
        src = str(ctx.message.channel)
        target = arg2.lower() + '-' + str(src.split('-')[1])
        newch = [a for a in bot.get_all_channels() if a.name == str(target)]
# And if it doesn't...
        if not newch:
# ...I'll send an error in a DM.
            await ctx.message.author.send('**Sorry, but...** The room you requested doesn\'t exist.')
            color.write('Whoops! They tried to move to a channel that doesn\'t exist.\n', 'COMMENT')
            return
# Otherwise...
# Next, I'll check to see if I need to ask for permission to get in.
        test = (str(arg2.lower()) == 'lobby' or str(arg2.lower()) == 'entroom')
        if test == False:
# If I do, I'll see if anybody else is in the channel.
            if len(newch[0].members) - 3 > 0:
# If there are people there, I'll ask for permission.
#                try:
#                    reactm = await newch[0].send(ctx.message.author.mention + ' wants to join the channel. One person must react within 10 seconds to accept.')
#                    await reactm.add_reaction('☑')
#                    def check(reaction, user):
#                        print(reaction.count, reaction.message.id == reactm.id, reaction.emoji)
#                        return reaction.count > 1 and reaction.message.id == reactm.id and str(reaction.emoji) == '☑'
#                    reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
#                    await reactm.delete()
#                except asyncio.TimeoutError:
#                    await reactm.delete()
#                    await ctx.message.author.send('Unfortunately, a channel member didn\'t let you in...')
#                    return
                await ctx.message.author.send('At this time, a Discord bug prevents me from asking for permission; as such, I can\'t add you right now. See #announcements for more info.')
                return
# Otherwise...
# All checks have passed, and I can begin.
# I'll start by taking the user's permissions for the source channel.
        source = ctx.message.channel
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages=False
        overwrite.read_messages=False
        await ctx.message.channel.set_permissions(ctx.message.author, overwrite=overwrite)
        color.write('Taken permissions for ' + str(source) + '...\n', 'COMMENT')
# Then, I'll send a message in the source channel, stating the user has left.
        name = ctx.message.author.mention
        response = str(name) + ' has left the room.'
        await ctx.send(response)
# Next, I'll send a message to the destination channel, stating the user has joined.
        name = ctx.message.author.mention
        response = str(name) + ' has entered the room.'
        destination = [a for a in bot.get_all_channels() if a.name == str(target)]
        await destination[0].send(response)
# Finally, I'll give the user access to the destination channel.
        floor = str(ctx.message.channel)
        target = arg2.lower() + '-' + str(floor.split('-')[1])
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages=True
        overwrite.read_messages=True
        await destination[0].set_permissions(ctx.message.author, overwrite=overwrite)
        color.write('Given permissions for ' + str(destination[0]) + '...\n', 'COMMENT')
# And now I'm done!
        color.write('And they\'re in the new room~\n\n', 'STRING')

## But...maybe they forgot arg1.
    elif arg1 == 'fail':
        await ctx.message.author.send('**Remember:** You need to type the following:\n```tnm!goto floor|room [floor number]|[room name]```')
        color.write('Confusion... ' + str(ctx.message.author) + ' tried to move, but didn\'t provide an arg1.\n\n', 'COMMENT')
        return
# Or, if they mistyped...
    else:
        err = '**Sorry, but...** I can only understand `floor` or `room` for the first argument. You said `' + str(arg1) + '`.'
        await ctx.message.author.send(err)
        color.write('Confusion... ' + str(ctx.message.author) + ' tried to move, but provided an invalid arg1. They tried to use `' + str(arg1) + '" .\n', 'COMMENT')
        return
bot.run(TOKEN)
