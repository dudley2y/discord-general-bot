import base64

with open("discordbot-83d1d-firebase-adminsdk-i3m7e-ff984a8634.json", "rb") as binary_file:
    binary_file_data = binary_file.read() 
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    print(base64_message)
    ### time to decode 
    with open("test.json", "wb") as file_to_save:
        decode_bytes = base64_message.encode('utf-8')
        decoded_data = base64.decodebytes(decode_bytes)
        file_to_save.write(decoded_data)
    




