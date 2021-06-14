import discord
import os
import sys
import base64
import atexit 
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
    print("We have logged in as " + client.user.name)


@client.event
async def on_voice_state_update(member, before, after):
    newMemberLiveRef = liveUsers_ref.child(str(member.id))
    if before.channel is None and after.channel is not None:
        newMemberLiveRef.set({"timeJoined": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})

    if before.channel is not None and after.channel is None:
       newMemberLiveRef.delete() 

    if after.channel is not None and after.channel!=before.channel:                                                                                                     ## "member" joins a voice channel
        userJoinedRef = users_ref.child(str(member.id)) 
        if userJoinedRef:                                                                                                             ## if the person exists in the database we want to send others a message
            recievers = userJoinedRef.child("reciever").get()                                                                          
            for reciever in recievers:                                                                                                ## for all users in the recieved list, send a message  
                user = client.get_user(reciever)
                if liveUsers_ref.child(str(reciever)).get() is not None: return 
                await user.send(str(member.name) + " joined " + after.channel.guild.name + " at " + after.channel.name)


@client.event
async def on_message(message): 
    if message.author == client.user:                                                                    ## if the message was sent by bot, disregard
        return 

    if message.content.startswith("-notifyMe"):                                                       

        nameOfUser = message.content.split("-notifyMe ",1)[1]                                            ## if the user is oneself, no point in adding self
        if nameOfUser == client.user.name: 
            await message.channel.send("Nice try, better luck next time")
            return 
        if nameOfUser == message.author.name:                                             
            await message.channel.send("Cannot add self to user list")
            return

        ## checks if added user is in the server
        newUser = None                                                                                   ## validates user looked up is in the server 
        async for user in message.guild.fetch_members(limit = message.guild.member_count):
            if user.name == nameOfUser:
                newUser = user
 
        if newUser == None:                                                                             ## couldn't find user in server 
            await message.channel.send("Could not find user, make sure you typed name correctly") 
            return
        
        ## check if user exists if not create
        
        newUserDbRef = users_ref.child(str(newUser.id))
 
        if newUserDbRef.get() == None:                                                                  ## adds user to database
            newUserDbRef.set({
                'user_name': newUser.name,
                'reciever': [message.author.id]
            })

            await message.channel.send("You have subscribed to " + nameOfUser)
        else: 
            user_reciever_list = newUserDbRef.child("reciever").get()                                  ## grabs old list of recievers

            if message.author.id in user_reciever_list:                                                ## checks for duplicates 
                await message.channel.send("You are already subscribed to this person")
                return

            user_reciever_list.append(message.author.id)                                               ## adds user to existing list 
            newUserDbRef.update({                                                                      ## updates it in database
                "reciever": user_reciever_list
            })

            await message.channel.send("You have subscribed to " + nameOfUser)

client.run(token)
