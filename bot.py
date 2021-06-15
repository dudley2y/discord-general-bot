import discord
import os
import sys
from firebase_admin import db 

import notifyMe  
import database

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

    if message.content.startswith("-notifyMe"):                                                       
        await notifyMe.notifyPreProcessing(client, message, users_ref)

    if message.content.startswith("-playVideo"):
        pass 
token = os.getenv("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else os.getenv("DISCORD_BOT_TOKEN")
client.run(token)
