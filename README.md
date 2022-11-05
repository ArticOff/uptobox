
# uptobox

A simple API wrapper for Uptobox.




## Authors

- [@ArticOff](https://www.github.com/ArticOff)


## Installation

Install uptobox with pip

```bash
# Linux/macOS
python3 -m pip install -U uptobox

# Windows
py -3 -m pip install -U uptobox
```
    
## Usage/Examples

```python
from uptobox import Client

client = Client(
    token="token"
)

@client.listen()
def on_connect():
    print(f"Connected to {client.user.name}")
    file = client.fetchFile("e9hrkzrylk58")
    print(file.name)
    client.upload("myfile.txt")

client.login()
```

## Feedback

If you have any feedback, please reach out to us on [our discord](https://articoff.github.io/discord)

## Links

- [Official discord server](https://articoff.github.io/discord)
- [CodeSec Community](https://articoff.github.io/codesec)
