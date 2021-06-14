import discord
import os
import sys
import base64
import atexit 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import notifyMe  

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.messages = True
intents.voice_states = True
client = discord.Client(intents=intents)

google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS").encode("utf-8")
decoded_credentials = base64.decodebytes(google_credentials)

with open(os.getenv("GOOGLE_FILE_PATH"), "wb") as google_credentials: 
    google_credentials.write(decoded_credentials)


atexit.register(os.remove, os.getenv("GOOGLE_FILE_PATH"))
cred = credentials.Certificate(os.getenv("GOOGLE_FILE_PATH"))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://discordbot-83d1d-default-rtdb.firebaseio.com/'
})


ref = db.reference('/')
users_ref = ref.child('users')
liveUsers_ref = ref.child('live')

token = os.getenv("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else os.getenv("DISCORD_BOT_TOKEN") 

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
    ##if message.content.startswith("-playVideo"):

token = os.getenv("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else os.getenv("DISCORD_BOT_TOKEN")
client.run(token)
