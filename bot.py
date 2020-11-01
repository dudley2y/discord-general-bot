import discord

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}\n".format(client))
    await messageTrish()

async def messageTrish():
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=15):
            if member.nick  == "Trish":
                channel = await member.create_dm()
                message = input(str("uwu boy: "))
                response = await member.send(message)

@client.event
async def on_message(message):
    if not message.author.bot:
        if message.author.name == "patcat":
            print("uwu girl: " +  message.content)
            await messageTrish()

client.run('NzY1NTA2MDE2NjY1Nzk2NjE4.X4VzCA.gYYWr-4tEu52LYlPnup_JKn3eF8')
# detect online / offline
# instagram scraper
# message image
# deploy to heroku

