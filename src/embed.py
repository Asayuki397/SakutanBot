from discord import Embed
import json

with open("profile.json", "r") as f:
    color = json.load(f)['color']

def create_embed(title, data , color = color):
    e = Embed(title = title, description= None, color = color)
    if type(data) == dict:
        for key in dict.keys():
            e.add_field(name = key, value = dict['key'], inline=False)

    elif type(data) == None:
        pass

    elif type(data) == list or tuple:
        for d in data:
            e.add_field(name=d, value = None, inline=False)

    else:
        e.add_field(name = data, value = None, inline = False)