from app import app
from flask import render_template, request, redirect, jsonify
import numpy as np
import base64
from io import BytesIO
from circuit import operational_amplifier, voltage_divider, current_divider, diode_characteristic_curve, half_wave_rectifier, full_wave_rectifier

circuitList = { 
        "1": "Voltage-Divider",
        "2": "Current-Divider",
        "3": "Diode-Characteristic-Curve",
        "4": "Half-Wave-Rectifier",
        "5": "Full-Wave-Rectifier",
    }
circuitImgList = {
    "1": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/voltage-divider.png",
    "2": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/current-divider.png",
    "3": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/diode-characteristic-curve-circuit.png",
    "4": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/half-wave-rectification.png",
    "5": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/full-wave-rectification.png",
}



@app.route("/", methods=["GET", "POST"])
def index():
    args = {}
    args['list'] = circuitList
    if request.args:
        raw_req = request.args
        item = raw_req['item']
        if item == "Voltage-Divider":
            args = {}
            args['list'] = circuitList
            imgUrl = circuitImgList.get("1")
            args['title'] = item
            args['imgUrl'] = imgUrl
            inputs = ['Vin', 'R1', 'R2']
            args['inputs'] = inputs
            msg = "Units: Vin = V , R1 & R2 = kOhm"
            args['msg'] = msg
            return render_template("circuit.html", args=args)

        if item == "Current-Divider":
            args = {}
            args['list'] = circuitList
            imgUrl = circuitImgList.get("2")
            args['title'] = item
            args['imgUrl'] = imgUrl
            inputs = ['Iin', 'R1', 'R2']
            args['inputs'] = inputs
            msg = "Units: Iin = A ,  R1 & R2 = kOhm"
            args['msg'] = msg
            return render_template("circuit.html", args=args)
            
        if item == "Diode-Characteristic-Curve":
            args = {}
            args['list'] = circuitList
            imgUrl = circuitImgList.get("3")
            args['title'] = item
            args['imgUrl'] = imgUrl
            args['inputs'] = ['Vin', 'R']
            msg = "Units: Vin = V ,  R = Ohm , Diode = '1N4148' "
            args['msg'] = msg
            return render_template("circuit.html", args=args)
        
        if item == "Half-Wave-Rectifier":
            args = {}
            args['list'] = circuitList
            imgUrl = circuitImgList.get("4")
            args['title'] = item
            args['imgUrl'] = imgUrl
            inputs = ['Vin', 'R' , 'C', 'F']
            args['inputs'] = inputs
            msg = "Units: Vin = V ,  R = Ohm , C = mF , F = Hz, Diode = '1N4148' "
            args['msg'] = msg
            return render_template("circuit.html", args=args)
        
        if item == "Full-Wave-Rectifier":
            args = {}
            args['list'] = circuitList
            imgUrl = circuitImgList.get("5")
            args['title'] = item
            args['imgUrl'] = imgUrl
            inputs = ['Vin', 'R' , 'C', 'F']
            args['inputs'] = inputs
            msg = "Units: Vin = V ,  R = Ohm , C = mF , F = Hz, Diode = '1N4148' "
            args['msg'] = msg
            return render_template("circuit.html", args=args)

  
    return render_template("index.html", args=args)

@app.route("/output", methods=["GET", "POST"])
def output():
    print('out')
    formData = request.form
    args = {}
    args['list'] = circuitList
    if formData['title'] ==  "Voltage-Divider":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, output = voltage_divider(formData['Vin'],formData['R1'],formData['R2'])
        args['title'] = circuit.title
        args['output'] = output
        inputs = str('Inputs: Vin = {} V , R1 = {} kOhm , R2 = {} kOhm'.format(formData['Vin'], formData['R1'], formData['R2']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)   

    if formData['title'] == "Current-Divider":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, output = current_divider(formData['Iin'],formData['R1'],formData['R2'])
        args['title'] = circuit.title
        args['output'] = output 
        inputs = str('Inputs: Iin = {} V , R1 = {} kOhm , R2 = {} kOhm'.format(formData['Iin'], formData['R1'], formData['R2']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)   

    if formData['title'] == "Diode-Characteristic-Curve":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = diode_characteristic_curve(formData['Vin'], formData['R'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} Ohm'.format(formData['Vin'], formData['R']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)
    
    if formData['title'] == "Half-Wave-Rectifier":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = half_wave_rectifier(formData['Vin'], formData['R'], formData['C'], formData['F'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} Ohm , C = {} mF, F = {} Hz'.format(formData['Vin'], formData['R'], formData['C'],formData['F']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)
    
    if formData['title'] == "Full-Wave-Rectifier":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = full_wave_rectifier(formData['Vin'], formData['R'], formData['C'], formData['F'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} Ohm , C = {} mF, F = {} Hz'.format(formData['Vin'], formData['R'], formData['C'],formData['F']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)


    return render_template("output.html", args=args)    

