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
    print(file.name)

@client.listen()
def on_logout():
    print("logout!")

@client.listen()
def on_error(error: ClientError):
    if isinstance(error, ClientError.NeedPremium):
        print("You're not a premium!")
    if isinstance(error, ClientError.PointsError):
        print("bro... you don't have the points...")
    if isinstance(error, ClientError.Warning):
        print(f"ouch: {error}")
    if isinstance(error, ClientError.InvalidParameter):
        print("There's an invalid parameter")

client.login()
