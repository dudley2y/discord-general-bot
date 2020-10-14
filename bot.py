import discord
from discord.utils import get

client = discord.Client()
intents = discord.Intents.default()
intents.members = True

ilc_guild = 705969305715474683
trish_id = 164555865171558402
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

    trish = await client.get_guild(ilc_guild).fetch_member(trish_id)
     
    async for member in client.get_guild(ilc_guild).fetch_members(limit=15):
        print(member.name, str(member.desktop_status))
        #if member.name == "jadb":
           # channel = await member.create_dm()
           # await channel.send("AL  i am SO good at programming")


client.run('NzY1NTA2MDE2NjY1Nzk2NjE4.X4VzCA.gYYWr-4tEu52LYlPnup_JKn3eF8')
