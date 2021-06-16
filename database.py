import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import base64
import atexit
import sys
from decouple import config

google_credentials = config("GOOGLE_APPLICATION_CREDENTIALS").encode("utf-8")
decoded_credentials = base64.decodebytes(google_credentials)
filePath = config("GOOGLE_FILE_PATH")

with open(filePath, "wb") as google_credentials:
    google_credentials.write(decoded_credentials)

atexit.register(os.remove, filePath)
cred = credentials.Certificate(filePath)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://discordbot-83d1d-default-rtdb.firebaseio.com/'
})
