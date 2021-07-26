# General Discord Bot

This is a general bot deployed on heroku that I'm gonna do whatever I feel like doing :-) 


## Installation and Prerequisites  

Use the package manager pip to install

```bash
pip install -U discord.py
pip install --user firebase-admin
pip install python-decouple
```

When running for the first time, there will be 4 environment variables necessary:
1. DISCORD_BOT_TOKEN = THE DISCORD BOT TOKEN
2. DISCORD_BOT_TEST_TOKEN = THE DISCORD TEST BOT TOKEN
3. GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-file.json
4. GOOGLE_FILE_PATH="file name to when running store credentials" 

Make sure you do run the first time with a `init` flag
## Usage 

Currently the bot can 
1. notify users when someone join a voicecall
2. nothing else hehe

Future plan
1. Stream youtube videos <- in progress

One can run the main bot using 
```bash
python bot.py
```

One can test using 
```bash
python bot.py test
```

Frist time running in test mode to add config 
```bash
python bot.py init test
```


## Architectures and Algorithms 

### message service v1 -> Done
```python
user_joined = user that joined
users_online[] 
for all channels:
    append all users currently in channels

for person in message file:
    if (person!= user_joined) and (user not in a channel):
        message person that user joined 
```

### message service v2 -> Done (Current) 
The user can opt into whoever they want notified, ideally be server independent

Preprocess: 
Member can use command  `-notifyMe [user] ` to add a user to their notify list 

```
1. check if user is in server and user is not self
2. check if user.id is in database, if not add to database
3. check if member is already in list, if not then add member.id to users recieve list
```

Algorithm 
```
1. recieve user joined call  
2. see if user is in notification database
3. for all recievers of user send message
```

database structure
```
    User: 
        recievers: ## everyone that gets a message when user joins a call
            1. 
            2. 
    User:
        recievers:
            1.
            2. 

```
    
## Commands

You must first create a text channel called `bot-commands` in order to use any
of the following commands. This can be changed in `bot.py`

#### -setAlarm (minutes) (youtube URL)    
Input a time in minute between 1 and 180 and sets the bot to activate an alarm once the selected time has passed. You can also put a youtube URL after the minutes to select a unique video for the alarm.

#### -listAlarms
List all alarms currently in the queue and provides alarm number, the name of the user who made it, and the time the alarm will go off. The time listed is based on the timezone set, default is UTC.

#### -delAlarm (alarm number)
Delete the alarm specified by the user. Alarm number is dictated by placement in the alarm list.

#### -clearList    
Clears the entire alarm list.

#### -setTZ (timezone offset)
Changes the displayed time according to the offset given. Based on UTC timezones, only offsets between -12 and 14 are allowed.

#### -setDefault (youtube URL)
Changes the default video that plays after the alarm time has elapsed.

#### -displayFormat
Toggle between 12 and 24-hour display format

#### -silence
Disconnects the bot from the voice channel it is currently connected to.
