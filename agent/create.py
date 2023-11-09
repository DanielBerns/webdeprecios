from getpass import getpass
from webclient import create_bot

user = input("User: ")
password = getpass(prompt="Your password: ")
response = create_bot(user, password)
print(response.status_code)
