from datetime import datetime

'''
notifyPreProcess( discordClient , message sent, database user_ref)

this function parses a user and adds the person who messaged about the user to a subscriber list,
verifies the user isn't 1.the bot 2. the messenger 3. isn't already subscribed. If the member is valid
and in the current guild, the user will be added to database if doesn't exist or if exists will have 
subscriber list updated
'''
async def notifyPreProcessing(client, message,  users_ref):
    
    nameOfUser = message.content.split("-notifyMe ", 1)[1] 

    if nameOfUser == client.user.name or nameOfUser == message.author.name:
        await message.channel.send("Nice try, better luck next time")
        return 

    newUser = message.guild.get_member_named(nameOfUser)

    if newUser == None: 
        await message.channel.send("Could not find user, make sure you typed name correctly") 
        return 

    newUserDbRef = users_ref.child(str(newUser.id)) 

    if newUserDbRef.get() == None:    
        newUserDbRef.set({
            'user_name': newUser.name,
            'reciever': [message.author.id]
        })

        await message.channel.send("You have subscribed to " + nameOfUser)

    else: 
        user_reciever_list = newUserDbRef.child("reciever").get()  
        if message.author.id in user_reciever_list: 
            await message.channel.send("You are already subscribed to this person")
            return 

        user_reciever_list.append(message.author.id)
        newUserDbRef.update({                                                                   
            "reciever": user_reciever_list
        })


''' 
notifyUsers( discordClient, User, voiceState, voiceState, database users_ref, database live_users_ref) 

messages people in the subscribed list that the User joined the call if they aren't 
already in a channel
'''

async def notifyUsers(client, member, before, after, users_ref, liveUsers_ref):
    newMemberLiveRef = liveUsers_ref.child(str(member.id)) 
    if before.channel is None and after.channel is not None:
        newMemberLiveRef.set({"timeJoined": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})

    elif before.channel is not None and after.channel is None:
         newMemberLiveRef.delete() 

    if after.channel is not None and after.channel!=before.channel:
        userJoinedRef = users_ref.child(str(member.id)) 
        
        if userJoinedRef:  
            recievers = userJoinedRef.child("reciever").get()  
            for reciever in recievers:
                user = client.get_user(reciever)
                if liveUsers_ref.child(str(reciever)).get() is not None: return 
                await user.send(str(member.name) + " joined " + after.channel.guild.name + " at " + after.channel.name)
