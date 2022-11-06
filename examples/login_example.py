from uptobox import (
    Client
)

client = Client(
    token="token"
)

@client.listen()
def on_connect():
    print(f"Connected to {client.user.name}")

client.login()
