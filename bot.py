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

new_user_ref = users_ref.child("bob2").get()

'''
new_user_ref.set({
    'messages': ["hello", "my", "name", "is", "josh"]
})
'''
ILC_guild_id = 705969305715474683

token = os.getenv("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else os.getenv("DISCORD_BOT_TOKEN") 

@client.event
async def on_ready():
    print("We have logged in as " + client.user.name)

@client.event
async def on_voice_state_update(member, before, after):

    if before.channel is None and after.channel is not None:    ## "member" joins a voice channel
        print(after.channel.guild)
        print(member.name + " joined a call")
        ilc = client.get_guild(ILC_guild_id) 
        channels = ilc.voice_channels                           ## grabs all channels in the server       
        curr_users = []                                         ## all users CURRENTLY in a voice channel
        member_channel_joined = None

        print("Current Users online: ", end = " ")
        for voice_channel in channels:                  
            for user in voice_channel.members:
                curr_users.append(user)
                if user == member:
                    member_channel_joined = voice_channel.name
                print(user.name + " " )


        with open("people.txt", "r") as people_file:
            while people_file:
                line = people_file.readline().rstrip()                   ## current memeber.name 
                curr_line_in_voice = False

                for user in curr_users:                         ## if the user currently is not in a voice channel
                    if user.name == line:
                        curr_line_in_voice = True                        

                if not curr_line_in_voice:
                    async for user in ilc.fetch_members(limit=ilc.member_count):
                        if user.name == line:
                            await user.send(str(member.name) + " joined ILC at " + str(member_channel_joined))
                            print("Sending " + user.name + " a message") 
                            break

@client.event
async def on_message(message): 
    if message.author == client.user:
        return 
    if message.content.startswith("-notifyMe"):
        userToBeAdded = message.content.split("-notifyMe ",1)[1]

        ## checks if added user is in the server 

        
        ## check if user exists if not create
        
        messagingUserRef = users_ref.child(message.author.id)

        if messagingUserRef.get() == None: 
            messagingUserRef.set({
                'user_name': message.author,
                'reciever': [userToBeAdded]
            })
        else: 
            messagingUserRef.update({
                'reciever': []
            })




client.run(token)
