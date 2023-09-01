"""
If you want to operate this software, this is the first program to run
"""

from pathlib import Path
import json
import uuid
import getpass
from typing import List
import logging

def get_constant(key: str, 
                 options: List[str], 
                 on_error: str) -> str:
    head = ', '.join(o for o in options)
    tail = f'any thing for {on_error:s}'
    message = f'{key:s} > {head:s} - {tail:s}: '
    source = input(message)
    try:
        k = options.index(source)
        return source
    except ValueError:
        return on_error


def get_name(key: str, 
             on_error: str, 
             characters: str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    source = input(key + ": ")
    if all(c in characters for c in source):
        return source
    else:
        return on_error


def get_custom_keys(file_identifier):
    try:
        with open(file_identifier, 'r') as source:
            custom_keys = json.load(source)
    except FileNotFoundError:
        print(f'{str(file_identifier):s} not found!')
        custom_keys = {'secret': [], 'public': []}
        with open(file_identifier, 'w') as target:
             json.dump(custom_keys, target)
    except json.decoder.JSONDecodeError:
        print(f'{str(file_identifier):s} bad json!')
        custom_keys = {'secret': [], 'public': []}
        with open(file_identifier, 'w') as target:
             json.dump(custom_keys, target)
             
    try:
        assert(isinstance(custom_keys['secret'], list))
        assert(isinstance(custom_keys['public'], list))
    except AssertionError:
        print(f'Not valid custom keys {str(custom_keys):s}')
        custom_keys = {'secret': [], 'public': []}
    return custom_keys


class Storage:
    
    @staticmethod
    def create_home_data_path(base: str, app_name: str) -> Path:
        home_data_path = Path('~', 'Data', base, app_name).expanduser()
        home_data_path.mkdir(mode=0o700, parents=True, exist_ok=True)
        return home_data_path
    
    @staticmethod
    def create_store_path(home_data_path: Path) -> Path:
        store_path = Path(home_data_path, 'store')
        store_path.mkdir(mode=0o700, parents=True, exist_ok=True)
        return store_path
    
    @staticmethod
    def create_logs_path(home_data_path: Path) -> Path:
        logs_path = Path(home_data_path, 'logs')
        logs_path.mkdir(mode=0o700, parents=True, exist_ok=True)
        return logs_path
    
    @staticmethod
    def create_dotenv(home_data_path: Path) -> Path:
        custom_keys = get_custom_keys(Path('custom_keys').with_suffix('.json'))
        dotenv_identifier = Path(home_data_path, 'env')
        with open(dotenv_identifier, 'w') as target:
            # Default key - value pairs
            key = "SECRET_KEY"
            value = uuid.uuid4().hex
            target.write(f'{key:s}="{value:s}"\n')
        
            key = "LOGGING_LEVEL"
            value = get_constant(key, ["CRITICAL", "ERROR", "WARNING", "INFO"], "DEBUG")
            target.write(f'{key:s}="{value:s}"\n')    
            
            # Custom key - value pairs
            for a_key in custom_keys['public']:
                value = input(a_key + ": ")
                target.write(f'{a_key:s}="{value:s}"\n')    
        
            for a_key in custom_keys['secret']:
                value = getpass.getpass(prompt=a_key + ": ")
                target.write(f'{a_key:s}="{value:s}"\n')

    
    @staticmethod
    def initialize(base: str, app_name: str) -> None:
        home_data_path = Storage.create_home_data_path(base, app_name)
        store_path = Storage.create_store_path(home_data_path)
        logs_path = Storage.create_logs_path(home_data_path)
        Storage.create_dotenv(home_data_path)
        print(f"         base: {base:s}")
        print(f"home_data_path: {str(home_data_path):s}")           
        print(f"   store_path: {str(store_path):s}")           
        print(f"    logs_path: {str(logs_path):s}")   

    @staticmethod    
    def main(base: str) -> None:
        Storage.initialize(base, 'server')
        Storage.initialize(base, 'client')
        Storage.initialize(base, 'ccc')

