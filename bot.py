import discord
import os
import sys
from firebase_admin import db 

import notifyMe  
import database
import alarm
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
    print("We have logged in!!!")


@client.event
async def on_voice_state_update(member, before, after):
    await notifyMe.notifyUsers(client, member, before, after, users_ref, liveUsers_ref)


@client.event
async def on_message(message): 
    if message.author == client.user:
        return 

    if message.channel.name != "bot-commands":
        return

    if message.content.startswith("-notifyMe"):                                                       
        await notifyMe.notifyPreProcessing(client, message, users_ref)

    if message.content.startswith("-playVideo"):
        pass

    if message.content.startswith("-setAlarm"):
        await alarm.alarmProcessing(message, client)
    
    if message.content.startswith("-listAlarms"):
        await alarm.listAlarms(message)

    if message.content.startswith("-clearList"):
        await alarm.clearList(message)

    if message.content.startswith("-setTZ"):
        await alarm.adjustTimezone(message)

    if message.content.startswith("-delAlarm"):
        await alarm.deleteAlarm(message)

    if message.content.startswith("-setDefault"):
        await alarm.changeDefaultUrl(message)

    if message.content.startswith("-silence"):
        await alarm.leave(message)
        
    if message.content.startswith("-displayFormat"):
        await alarm.changeFormat(message)

token = config("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else config("DISCORD_BOT_TOKEN")
client.run(token)
