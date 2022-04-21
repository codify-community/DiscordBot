import os
import json

path = os.getcwd()

def get_json(json_file):
    with open(f"{path}/{json_file}") as file:
        return json.load(file)