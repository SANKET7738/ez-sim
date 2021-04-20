from app import app
from flask import render_template, request, redirect, jsonify
import numpy as np
import base64
from io import BytesIO
from circuit import operational_amplifier, voltage_divider, current_divider

circuitList = { 
        "1": "Voltage-Divider",
        "2": "Current-Divider"
    }
circuitImgList = {
    "1": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/voltage-divider.png",
    "2": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/current-divider.png",
}

args = {}
args['list'] = circuitList

@app.route("/", methods=["GET", "POST"])
def index():
    if request.args:
        raw_req = request.args
        item = raw_req['item']
        if item == "Voltage-Divider":
            imgUrl = circuitImgList.get("1")
            args['title'] = item
            args['imgUrl'] = imgUrl
            return render_template("circuit.html", args=args)
        if item == "Current-Divider":
            imgUrl = circuitImgList.get("2")
            args['title'] = item
            args['imgUrl'] = imgUrl
            return render_template("circuit.html", args=args)
  
    return render_template("index.html", args=args)

@app.route("/output", methods=["GET", "POST"])
def output():
    print('out')
    formData = request.form
    if formData['title'] ==  "Voltage-Divider":
        circuit, analysis, output = voltage_divider(formData['Vin'],formData['R1'],formData['R2'])
        args['title'] = circuit.title
        args['output'] = output
        return render_template("output.html", args=args)   

    if formData['title'] == "Current-Divider":
        circuit, analysis, output = current_divider(formData['Vin'],formData['R1'],formData['R2'])
        args['title'] = circuit.title
        args['output'] = output
        return render_template("output.html", args=args)    

    return render_template("output.html", args=args)    

