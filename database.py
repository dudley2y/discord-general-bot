import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import base64
import atexit

google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS").encode("utf-8")
decoded_credentials = base64.decodebytes(google_credentials)

with open(os.getenv("GOOGLE_FILE_PATH"), "wb") as google_credentials:
    google_credentials.write(decoded_credentials)

atexit.register(os.remove, os.getenv("GOOGLE_FILE_PATH"))
cred = credentials.Certificate(os.getenv("GOOGLE_FILE_PATH"))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://discordbot-83d1d-default-rtdb.firebaseio.com/'
})
