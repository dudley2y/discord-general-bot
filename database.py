import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import base64
import atexit
import sys
import json
from decouple import config

initialize = False

for x in sys.argv:
    if x == "init":
        initialize = True

if initialize:
    envFile = open(".env", "w")
    print ("Init Setup")
    
    google_credentials_file = input("Enter Google Application Credentials: ")
    with open(google_credentials_file) as gFile:
         jsonData = json.load(gFile) 
         jsonCred = json.dumps(jsonData).encode("utf-8") 
         envFile.write("GOOGLE_APPLICATION_CREDENTIALS="+ jsonCred + "\n")


    envFile.write("GOOGLE_APPLICATION_CREDENTIALS="+google_credentials_file+"\n")

    filePath = input("Enter Google File Path: ")
    envFile.write("GOOGLE_FILE_PATH="+filePath+"\n")

    botToken = input("Enter Discord Bot Token: ")
    envFile.write("DISCORD_BOT_TOKEN="+botToken+"\n")

    botTestToken = input("Enter Discord Bot Test Token: ")
    envFile.write("DISCORD_BOT_TEST_TOKEN="+botTestToken+"\n")

    envFile.close()


filePath = config("GOOGLE_FILE_PATH")

with open(filePath, "w") as google_credentials:
    google_credentials.write(config("GOOGLE_APPLICATION_CREDENTIALS"))

atexit.register(os.remove, filePath)
cred = credentials.Certificate(filePath)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://discordbot-83d1d-default-rtdb.firebaseio.com/'
})
