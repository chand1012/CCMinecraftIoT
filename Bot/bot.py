import discord
import json
import requests

def get_keys(filename="keys.json"):
    parsed = None
    with open(filename) as keyfile:
        raw = keyfile.read()
        parsed = loads(raw)
    return parsed
