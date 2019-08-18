from flask import Flask, Response, request
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    devices = os.listdir("devices")
    dictlist = []
    for device in devices:
        f = open("devices/"+device)
        d = json.loads(f.read())
        f.close()
        dictlist += [d]
    return json.dumps(dictlist)
    
@app.route("/<string:name>")
def getbyname(name):
    rtrstr = ""
    filename = "devices/" + name + ".json"
    f = open(filename)
    rtrstr = f.read()
    f.close()
    return rtrstr

@app.route("/request", methods=["POST"])
def savedata():
    dict_data = request.get_json(force=True)
    filename = "devices/" + dict_data.get("name") + ".json"
    f = open(filename, 'w')
    f.write(json.dumps(dict_data))
    f.close()
    return Response(status=200)

if __name__=="__main__":
    app.run("0.0.0.0", 8080)