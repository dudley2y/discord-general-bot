import discord

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.voice_states = True
client = discord.Client(intents=intents)

ILC_guild_id = 705969305715474683

@client.event
async def on_ready():
    print("We have logged in as {0.user}\n".format(client))

@client.event
async def on_voice_state_update(member, before, after):

    isInList = False
    with open("people.txt", "r") as file:
        while file:
            line = file.readline().rstrip()
            if line == member.name:
                isInList = True

    if before.channel is None and after.channel is not None and isInList :    ## "member" joins a voice channel
        
        print(member.name + " joined a call")


        if isInList:
            ilc = client.get_guild(ILC_guild_id) 
            channels = ilc.voice_channels                           ## grabs all channels in the server       
            curr_users = []                                         ## all users CURRENTLY in a voice channel

            for voice_channel in channels:                  
                for user in voice_channel.members:
                    curr_users.append(user)

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
                                await user.send(str(member) + " joined ILC")
                                break

client.run('NzY1NTA2MDE2NjY1Nzk2NjE4.X4VzCA.gYYWr-4tEu52LYlPnup_JKn3eF8')

'''
1. see if a person joined a voice_channel
2. alert everyone that's either 
    a. not in the call
    b. not the same person

    that a person joined the voice_channel

'''