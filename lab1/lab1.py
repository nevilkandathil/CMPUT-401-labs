import requests


print(requests.__version__)


res = requests.get("https://raw.githubusercontent.com/nevilkandathil/CMPUT-401-labs/main/lab1/lab1.py")

print(res.text)
