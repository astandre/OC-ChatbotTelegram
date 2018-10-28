import requests
from decouple import config

BASE_URL = config("BASE_URL")
CONNECTION_KEY = config("CONNECTION_KEY")


def init_chatbot():
    url = BASE_URL + '/init/'
    json = {'key': CONNECTION_KEY}
    r = requests.post(url, json=json)
    if r.status_code == 200:
        response = r.json()
        print("\nSuccessfully connected to system")
        print(response)
        commands_raw = response["commands"]
        commands_simple = []
        commands_full = ""
        for command in commands_raw:
            command_name = "/" + command["name"]
            commands_simple.append([command_name])
            command_full = "- " + command_name + ": " + command["description"] + ". \n"
            commands_full += command_full
        response = {"simple": commands_simple, "full": commands_full}
    else:
        print(r)
        response = None
    return response


def chat_with_system(data):
    url = BASE_URL + '/init/'
    json = {'key': CONNECTION_KEY, "content": data["content"]}
    r = requests.post(url, json=json)
    if r.status_code == 200:
        response = r.json()
        print(response)
    else:
        print(r)
        response = None
    return response
