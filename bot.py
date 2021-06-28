import discord
from discord.ext import commands
import os
import sys
from firebase_admin import db 

import notifyMe  
import database
from decouple import config

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.messages = True
intents.voice_states = True
client = discord.Client(intents=intents)

ref = db.reference('/')
users_ref = ref.child('users')
liveUsers_ref = ref.child('live')

@client.event
async def on_ready():
    print("We have logged in as "+ client.user.name + "!!!")


@client.event
async def on_voice_state_update(member, before, after):
    # await notifyMe.notifyUsers(client, member, before, after, users_ref, liveUsers_ref)
    if after.channel is not None:
        name = member.display_name
        textChannelList = member.guild.text_channels
        for textChannel in textChannelList:
            if textChannel.name == 'bot-log':
                await textChannel.send('Hello, '+ name + '!')
                break
    if after.channel is None and before.channel is not None:
        name = member.display_name
        await member.guild.text_channels[1].send('Goodbye, '+ name + '!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith("-notifyMe"):                                                       
        await notifyMe.notifyPreProcessing(client, message, users_ref)

    if message.content.startswith("-playVideo"):
        pass 

    if message.content.startswith("-reply"):
        await message.channel.send('Bot sent a message')

token = config("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else config("DISCORD_BOT_TOKEN")
client.run(token)
