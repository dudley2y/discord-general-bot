# General Discord Bot

This is a general bot deployed on heroku that I'm gonna do whatever I feel like doing :) 

## Installation and Prerequisites  

Use the package manager pip to install discord.py 

```bash
python3 -m pip install -U discord.py
```

There will be 2 environment variables necessary to update in start.sh
1. DISCORD_BOT_TOKEN = THE DISCORD BOT TOKEN
2. DISCORD_BOT_TEST_TOKEN = THE DISCORD TEST BOT TOKEN

## Usage 

Currently the bot can 
1. notify users when someone join's ILC 
2. nothing else hehe

Future plan
1. Stream youtube videos

One can run the main bot using 
```bash
python bot.py
```

One can test using 
```bash
python bot.py test
```


## Architectures and Algorithms 

### message service
```python
user_joined = user that joined
users_online[] 
for all channels:
    append all users currently in channels

for person in message file:
    if (person!= user_joined) and (user not in a channel):
        message person that user joined 
```

### message service v2 <- in progress
The user can opt into whoever they want notified, ideally be server independent

Preprocess: 
Member can use command  ```bash -notifyMe [user] ``` to add a user to their notify list 

```
1. check if user is in server
2. check if Member.id is in database, if not add to database
3. add user to Member's id to reciever list 
```

Algorithm 
```
1. recieve user joined call 
2. for all recievers: send message
```

database structure
```
    User: 
        recievers: 
            1. 
            2. 
    User:
        recievers:
            1.
            2. 

```
    
