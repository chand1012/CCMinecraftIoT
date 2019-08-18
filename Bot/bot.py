import discord
import json
import requests

def get_keys(filename="token.json"):
    parsed = None
    with open(filename) as keyfile:
        raw = keyfile.read()
        parsed = json.loads(raw)
    return parsed

def get_status():
    response = requests.get("http://localhost:8080")
    data = json.loads(response.text)
    return data

keys = get_keys()
token = keys['token']
client = discord.Client()

@client.event
async def on_message(message):
    recv = message.content
    if message.author == client.user:
        return
    if recv.lower().startswith('!cciot'):
        if recv[7:]=='':
            status = get_status()
            msg = ''
            for thing in status:
                msg += thing["name"].capitalize() + "\n"
                for k in thing:
                    if k != "name":
                        msg += k + " = " + str(thing[k]) + "\n"
            print(msg)
            await message.channel.send(content=msg)
        else:
            args = recv.split(" ")
            if args[1]=="get":
                response = requests.get("http://localhost:8080/"+args[2])
                thing = json.loads(response.text)
                msg = thing["name"].capitalize() + "\n"
                for k in thing:
                    if k != "name":
                        msg += k + " = " + str(thing[k]) + "\n"
                print(msg)
                await message.channel.send(content=msg)
            else:
                response = requests.get("http://localhost:8080/"+args[2])
                thing = json.loads(response.text)
                value = thing.get(args[3])
                if value is None:
                    msg = "Error: value does not exist!"
                else:
                    if any(char.isdigit() for char in args[4]):
                        thing[args[3]] = int(args[4])
                    elif args[4]=="false":
                        thing[args[3]] = False
                    elif args[4]=="true":
                        thing[args[3]] = True
                    else:
                        thing[args[3]] = args[4]
                    response = requests.post("http://localhost:8080/"+args[2], data=json.dumps(thing))
                    if response.status_code != 200:
                        msg = "Error: " + str(response.status_code)+"."
                    else:
                        msg = "Value " + args[3] + " changed to " + args[4] + "."
                await message.channel.send(content=msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

while True:
    try:
        client.run(token)
    except Exception as e:
        if "Event loop" in str(e):
            print("\nStopping bot....")
            break
        else:
            print(e)
            continue
