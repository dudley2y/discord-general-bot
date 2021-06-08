# General Discord Bot

This is a general bot deployed on heroku that I'm gonna do whatever I feel like doing :) 

## Installation and Prerequisites  

Use the package manager pip to install discord.py 

```bash
python3 -m pip install -U discord.py
```

There will be 2 environment variables necessary 
1. DISCORD_BOT_TOKEN
2. DISCORD_BOT_TEST_TOKEN

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
    
