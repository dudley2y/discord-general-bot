import discord
import os
import sys

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.voice_states = True
client = discord.Client(intents=intents)

ILC_guild_id = 705969305715474683

token = os.getenv("DISCORD_BOT_TEST_TOKEN") if sys.argv[-1] == "test" else os.getenv("DISCORD_BOT_TOKEN") 

@client.event
async def on_ready():
    print("We have logged in as " + client.user.name)

@client.event
async def on_voice_state_update(member, before, after):

    if before.channel is None and after.channel is not None:    ## "member" joins a voice channel
        
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

client.run(token)

