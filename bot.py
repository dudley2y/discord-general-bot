import discord
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.messages = True
intents.voice_states = True
client = discord.Client(intents=intents)

cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://discordbot-83d1d-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')
users_ref = ref.child('users')

token = os.getenv("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else os.getenv("DISCORD_BOT_TOKEN") 

@client.event
async def on_ready():
    print("We have logged in as " + client.user.name)

@client.event
async def on_voice_state_update(member, before, after):

    if after.channel is not None:    ## "member" joins a voice channel
        userJoinedRef = users_ref.child(str(member.id)) 
        if userJoinedRef:
            recievers = userJoinedRef.child("reciever").get() 
            for reciever in recievers:
                user = client.get_user(reciever) 
                await user.send(str(member.name) + " joined " + after.channel.guild.name + " at " + after.channel.name)


@client.event
async def on_message(message): 
    if message.author == client.user:
        return 

    if message.content.startswith("-notifyMe"):

        nameOfUser = message.content.split("-notifyMe ",1)[1]

        if nameOfUser == message.author.name: 
            await message.channel.send("Cannot add self to user list")
            return

        ## checks if added user is in the server
        newUser = None
        async for user in message.guild.fetch_members(limit = message.guild.member_count):
            if user.name == nameOfUser:
                newUser = user

        if newUser == None:
            await message.channel.send("Could not find user, make sure you typed name correctly") 
            return
        
        ## check if user exists if not create
        
        newUserDbRef = users_ref.child(str(newUser.id))

        if newUserDbRef.get() == None: 
            newUserDbRef.set({
                'user_name': newUser.name,
                'reciever': [message.author.id]
            })
        else: 
            user_reciever_list = newUserDbRef.child("reciever").get()

            if message.author.id in user_reciever_list:
                await message.channel.send("You are already subscribed to this person")
                return

            user_reciever_list.append(message.author.id)
            newUserDbRef.update({
                "reciever": user_reciever_list
            })

client.run(token)
