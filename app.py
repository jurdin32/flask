from flask import Flask, render_template, make_response, jsonify, request

app =Flask(__name__)
PORT = 4000
HOST = '0.0.0.0'

INFO ={
    "languages":{
        "es":"Spanish",
        "en":"English",
        "fr":"French"
    },
    "colors":{
        "r":"red",
        "b":"blue",
        "o":"orange"
    },
    "clouds":{
        "IBM":"IBM Cloud",
        "AMAZON":"AWS",
        "MICROSOFT":"AZURE",
    }
}


@app.route("/")



def home():
    return "<h1>Hola mundo</h1>"


@app.route("/temp")
def template():
    return render_template('index.html')


@app.route("/qstr")
def query_string():
    if request.args:
        req=request.args
        res={}
        for key, value in req.items():
            res[key] =value
        res =make_response(jsonify(res),200)
        return res
    res=make_response(jsonify({"error":"No hay argumentos"}),400)
    return res

@app.route("/json")
def get_json():
    res=make_response(jsonify(INFO),200)
    return res

@app.route("/json/<collection>/<member>")
def get_data(collection, member):
    if collection in INFO:
        member = INFO[collection].get(member)
        if member:
            res =make_response(jsonify({"res":member}),200)
            return res
    res=make_response(jsonify({"error":"No hay Members"}),400)
    return res

#POST
@app.route("/json/<collection>",methods=["POST"])
def create_collection(collection):
    req=request.get_json()

    if collection in INFO:
        res=make_response(jsonify({"error":"La coleccion ya existe"}),400)
        return res
    
    INFO.update({collection:req})

    res= make_response(jsonify({"message":"Coleccion creada"}),201)
    return res

#PUT:
@app.route("/json/<collection>/<member>",methods=["PUT"])
def update_collection(collection,member):
    req=request.get_json()

    if collection in INFO:
        if member:
            INFO[collection][member]=req["new"] # => se usa para enviar el parametro
            res=make_response(jsonify({"res":INFO[collection]}),200)
            return res
        
        res= make_response(jsonify({"error":"No hay miembro"}),400)
        return res
    
    res= make_response(jsonify({"error":"Sin conexion "}),400)
    return res

@app.route("/json/<collection>", methods=["DELETE"])
def delete_collection(collection):

    if collection in INFO:
        del INFO[collection]
        res=make_response(jsonify(INFO),200)
        return res

    res=make_response(jsonify({"error":"ya no existe la coleccion"}),400)
    return res




if __name__ == "__main__":
    print("Servidor corriendpo %s"%(PORT))
    app.run(host=HOST,port=PORT)