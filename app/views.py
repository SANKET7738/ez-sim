from app import app
from flask import render_template, request, redirect, jsonify
import numpy as np
import base64
from io import BytesIO
from circuit import operational_amplifier, voltage_divider

circuitList = { 
        "1": "Voltage Divider",
        "2": "Current Divider"
    }
circuitImgList = {
    "1": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/voltage-divider.png",
    "2": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/current-divider.png",
}

@app.route("/", methods=["GET", "POST"])
def index():
    args = {}
    args['list'] = circuitList
    if request.args:
        raw_req = request.args
        item = raw_req['item']
        if item == "Voltage Divider":
            imgUrl = circuitImgList.get("1")
            args['title'] = item
            args['imgUrl'] = imgUrl
            return render_template("circuit.html", args=args)
        if item == "Current Divider":
            imgUrl = circuitImgList.get("2")
            args['title'] = item
            args['imgUrl'] = imgUrl
            return render_template("circuit.html", args=args)

    # circuit, analysis, plt = operational_amplifier()
    # print(circuit.title)
    # for i in analysis.frequency:
    #     print(i)
    # print(20*np.log10(np.absolute(analysis.out)))
    # plt.show(block=True)
    # buf = BytesIO()
    # plt.savefig(buf, format="png")
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    circuit, analysis, output = voltage_divider()
    args['title'] = circuit.title
    args['output'] = output
  
    return render_template("index.html", args=args)

@app.route("/output", methods=["GET", "POST"])
def output():
    print(request)
    return render__template("output.html", args)

