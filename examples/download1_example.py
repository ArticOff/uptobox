from uptobox import (
    Client,
    ClientError
)

client = Client(
    token="token"
)

@client.listen()
def on_connect():
    print(f"Connected to {client.user.name}")
    file = client.fetchFile("e9hrkzrylk58")
    print(file.downloadURL)

client.login()
