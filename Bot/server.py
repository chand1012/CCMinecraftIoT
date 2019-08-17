from flask import Flask, Response, request
import json

filename = "ccdata.json"

app = Flask(__name__)

@app.route("/")
def index():
    rtrstr = ""
    f = open(filename)
    rtrstr = f.read()
    f.close()
    return rtrstr

@app.route("/request", methods=["GET","POST"])
def savedata():
    if request.method == "POST":
        dict_data = request.get_json(force=True)
        #dict_data = json.loads(data)
        f = open(filename)
        current_data = json.loads(f.read())
        f.close()
        for k in current_data:
            if not k in dict_data or dict_data[k]!=current_data[k]:
                current_data[k] = dict_data.get(k)
        f = open(filename, 'w')
        f.write(json.dumps(current_data))
        f.close()
        return Response(200)
    else:
        f = open(filename)
        data = f.read()
        f.close()
        return data

if __name__=="__main__":
    app.run("0.0.0.0", 8080)