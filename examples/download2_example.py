from uptobox import (
    Client
)

client = Client(
    token="token"
)

@client.listen()
def on_connect():
    print(f"Connected to {client.user.name}")
    file = client.fetchFile("e9hrkzrylk58")
    client.download(file.code)

client.login()
