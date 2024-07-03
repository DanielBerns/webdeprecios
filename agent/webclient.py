import json
from random import choices
from pathlib import Path 
import os
from typing import Dict, Tuple, Generator

import requests

AuthHeaders = requests.structures.CaseInsensitiveDict
Response = requests.Response


identifier: str = os.environ.get("ATHENA_IDENTIFIER") or "random"
password: str = os.environ.get("ATHENA_PASSWORD") or "1123581321"
website: str = "https://webdeprecios.unp.edu.ar"

store_path: Path = Path("~", "Info", "athena", "webclient", "store", identifier).expanduser()
store_path.mkdir(mode=0o700, parents=True, exist_ok=True)
log_switches: Path = Path(store_path, "switches.md").expanduser()  
with open(log_switches, "w") as target:
    target.write(f"identifier {identifier:s}\n"
                 f"website {website:s}\n"
                )


create_user_url: str = f"{website:s}/api/users"
tokens_url: str = f"{website:s}/api/tokens"
current_user_url: str = f"{website:s}/api/users/current"
all_the_messages_url: str = f"{website:s}/api/messages/all"
empty_messages_url: str = f"{website:s}/api/messages/empty"
publish_post_url: str = f"{website:s}/api/posts"
get_post_url = lambda id_: f"{website:s}/api/posts/{id_:d}"
delete_post_url = lambda id_: f"{website:s}/api/posts/{id_:d}"


def create_user(username: str, password: str) -> Response:
    payload: Dict[str, str] = {"username": username, 
                               "password": password}
    response = requests.post(
        create_user_url, 
        json=payload)
    return response


def login_bot(username: str, password: str) -> Response:
    return requests.post(
        tokens_url, 
        auth=requests.auth.HTTPBasicAuth(username, password))


def get_token_headers(token: str) -> AuthHeaders:
    auth_headers = AuthHeaders()
    auth_headers["Accept"] = "application/json"
    auth_headers["Authorization"] = f"Bearer {token}"
    return auth_headers


def get_current_user(auth_headers: AuthHeaders) -> Response:
    return requests.get(
        current_user_url, 
        headers=auth_headers)


# https://forpythons.com/how-to-upload-file-with-python-requests/

class WebClientException(Exception):
    pass

def publish_post(auth_headers: AuthHeaders, content: str) -> Response:
    payload = {"content": content}
    response = requests.post(publish_post_url, 
                             headers=auth_headers, 
                             json=payload)
    return response

def get_post(auth_headers: AuthHeaders, id_: int) -> Response:
    the_url = get_post_url(id_)
    response = requests.get(the_url, headers=auth_headers)
    return response

def empty_data(file_identifier: Path) -> Dict[str, str]:
    custom_data = {"username": "", "password": "", "register": ""}
    with open(file_identifier, "w") as target:
         json.dump(custom_data, target)
    return custom_data


def load_data(file_identifier: Path) -> Dict[str, str]:
    try:
        with open(file_identifier, "r") as source:
            some_data = json.load(source)
    except FileNotFoundError:
        print(f"{str(file_identifier):s} not found!")
        some_data = empty_data(file_identifier)
    except json.decoder.JSONDecodeError:
        print(f"{str(file_identifier):s} bad json!")
        some_data = empty_data(file_identifier)
    return some_data


def write_data(some_data: Dict[str, str], file_identifier: Path) -> None:
    with open(file_identifier, "w") as target:
         json.dump(some_data, target)


def report(response: Response) -> None:
    status_code = response.status_code
    text = response.text
    print("status_code", status_code)
    print("*"*80)
    print(text)
    print("*"*80)                


def generate_secret_data(secret_data_file_identifier: Path) -> Dict[str, str]:
    randombot_data = load_data(secret_data_file_identifier)
    source = "abcdefghijklmnopqrstuvwxyz0123456789_()-+~"
    secret_data = {}
    secret_data["username"] = "".join(choices(source, k=10))
    secret_data["password"] = "".join(choices(source, k=10))
    secret_data["register"] = "yes"
    write_data(secret_data, secret_data_file_identifier)
    return secret_data


def get_secret_fields(secret_data: Dict[str, str]) -> Tuple[str, str, str]:
    try:
        username, password, register = secret_data["username"], secret_data["password"], secret_data["register"]
    except KeyError as message:
        print("Error", str(message), "-", str(secret_data))
        username, password, register = "", "", ""
    return username, password, register


def get_all_the_messages(auth_headers: AuthHeaders) -> Response:
    return requests.get(all_the_messages_url, headers=auth_headers)

def get_all_the_posts(auth_headers: AuthHeaders) -> Response:
    return requests.get(all_the_posts_url, headers=auth_headers)

def clear_message_queue(auth_headers: AuthHeaders) -> Response:
    return requests.get(empty_messages_url, headers=auth_headers)


def get_auth_headers(username: str) -> AuthHeaders:
    if username == "random":
        username = "randombot"
        secret_data_file_identifier = Path(store_path, username + ".json")
        if secret_data_file_identifier.exists():
            secret_data = load_data(secret_data_file_identifier)
        else:
            secret_data = generate_secret_data(secret_data_file_identifier)
    else:
        secret_data_file_identifier = Path(store_path, username + ".json")
        if secret_data_file_identifier.exists():
            secret_data = load_data(secret_data_file_identifier)
        else:
            secret_data = generate_secret_data(secret_data_file_identifier)
            secret_data["username"] = username
            write_data(secret_data, secret_data_file_identifier)
    username, password, register = get_secret_fields(secret_data)
    auth_headers = None
    try:
        if len(username) == 0:
            raise ValueError("username unexpected null value")
        if len(password) == 0:
            raise ValueError("password unexpected null value")
        if  register == "yes":
            print("Register")
            response = create_user(username, password)
            report(response)
            secret_data["user"] = response.json()
            secret_data["register"] = "no"
            write_data(secret_data, secret_data_file_identifier)
        elif register == "no":
            print("No need to register user")
        else:
            raise ValueError(f"register unexpected value {register:s}")
    except ValueError as message:
        print("Error", str(message))
    else:
        print("Getting authentication token")
        response = login_bot(username, password)
        report(response)
        if response.status_code == 200:
            print("Logged in")
            token_json = response.json()
            token = token_json["token"]
            print("Got the token", token)
            auth_headers = get_token_headers(token)
    return auth_headers


def get_messages(auth_headers: AuthHeaders) -> Generator[Dict[str, str], None, None]:    
    if auth_headers:
        print("Get current user received messages")
        response = get_all_the_messages(auth_headers)
        as_json = response.json()
        for message in as_json["items"]:
            yield message


def clear_messages(auth_headers: AuthHeaders) -> None:    
    if auth_headers:
        response = clear_message_queue(auth_headers)
        print(response.status_code)
        print(response.text)
