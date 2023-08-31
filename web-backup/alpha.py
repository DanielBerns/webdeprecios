"""
If you want to use this web, install the server with this program.
"""

from pathlib import Path
import json
import uuid
import getpass
from typing import List


def get_constant(source: str, 
                 options: List[str], 
                 on_error: str) -> str:
    try:
        k = options.index(source)
        return source
    except ValueError:
        return on_error


def get_name(source: str, 
             on_error: str, 
             characters: str ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    if all(c in characters for c in source):
        return source
    else:
        return on_error


def get_custom_keys(file_identifier):
    try:
        with open(Path('./alpha.json'), 'r') as source:
            custom_keys = json.load(source)
    except FileNotFoundError:
        custom_keys = {'secret': [], 'public': []}
    return custom_keys


print('Creating dot server folder')
print('Configuring server')


root_path = Path('~', '.server').expanduser()
store_path = Path(root_path, 'store')
store_path.mkdir(mode=0o700, parents=True, exist_ok=True)

custom_keys = get_custom_keys('./custom_keys.json')

file_identifier = Path(root_path, 'env')
with open(file_identifier, 'w') as target:
    key = "SECRET_KEY"
    value = uuid.uuid4().hex
    target.write(f'{key:s}="{value:s}"\n')

    key = "LOGGING_LEVEL"
    source = input(key + " (any thing for debug): ")
    value = get_constant(source, ["CRITICAL", "ERROR", "WARNING", "INFO"], "DEBUG")
    target.write(f'{key:s}="{value:s}"\n')    
    
    key = "WEBSITE"
    source = input(key + ": ")
    value = get_name(source, "website")
    target.write(f'{key:s}="{value:s}"\n')    

    for a_key in custom_keys['public']:
        value = input(a_key + ": ")
        target.write(f'{a_key:s}="{value:s}"\n')    

    for a_key in custom_keys['secret']:
        value = getpass.getpass(prompt=a_key + ": ")
        target.write(f'{a_key:s}="{value:s}"\n')
