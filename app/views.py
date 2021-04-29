from app import app
from flask import render_template, request, redirect, jsonify
import numpy as np
import base64
from io import BytesIO
from circuit import operational_amplifier, voltage_divider, current_divider, diode_characteristic_curve, half_wave_rectifier, full_wave_rectifier, low_pass_rc_filter, high_pass_rc_filter, series_negative_clipper, series_positive_clipper, positive_clamper, negative_clamper, nmos_characteristics

circuitList = { 
        "1": "Voltage-Divider",
        "2": "Current-Divider",
        "3": "Diode-Characteristic-Curve",
        "4": "Half-Wave-Rectifier",
        "5": "Full-Wave-Rectifier",
        "6": "Low-Pass-RC-Filter",
        "7": "High-Pass-RC-Filter",
        "8" : "Series-Negative-Clipper",
        "9" : "Series-Positive-Clipper",
        "10" : "Positive-Clamper",
        "11" : "Negative-Clamper",
        "12" : "n-MOSFET-Characteristics",
    }
circuitImgList = {
    "Voltage-Divider": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/voltage-divider.png",
    "Current-Divider": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/current-divider.png",
    "Diode-Characteristic-Curve": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/diode-characteristic-curve-circuit.png",
    "Half-Wave-Rectifier": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/half-wave-rectification.png",
    "Full-Wave-Rectifier": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/full-wave-rectification.png",
    "Low-Pass-RC-Filter": "https://pyspice.fabrice-salvaire.fr/releases/v1.4/_images/low-pass-rc-filter.png",
    "High-Pass-RC-Filter": "https://www.electronics-tutorials.ws/wp-content/uploads/2013/08/fil11.gif?fit=326%2C165",
    "Series-Negative-Clipper": "https://www.daenotes.com/sites/default/files/article-images/series-negative-clipper.GIF",
    "Series-Positive-Clipper" : "https://www.daenotes.com/sites/default/files/article-images/series-positive-clipper.GIF",
    "Positive-Clamper" : "https://www.tutorialspoint.com/electronic_circuits/images/positive_clamper_circuit.jpg",
    "Negative-Clamper" : "https://www.tutorialspoint.com/electronic_circuits/images/negative_clamper_circuit.jpg",
    "n-MOSFET-Characteristics" : "http://www.physics.csbsju.edu/trace/i/nMOSFET.CC.gif",
}

inputList = {
    "Voltage-Divider" : [['Vin', 'R1', 'R2'], "Units: Vin = V , R1 & R2 = kOhm" ],
    "Current-Divider" : [['Iin', 'R1', 'R2'], "Units: Iin = A ,  R1 & R2 = kOhm" ],
    "Diode-Characteristic-Curve" : [['Vin', 'R'], "Units: Vin = V ,  R = Ohm , Diode = '1N4148' "],
    "Half-Wave-Rectifier" : [['Vin', 'R' , 'C', 'F'], "Units: Vin = V ,  R = Ohm , C = mF , F = Hz, Diode = '1N4148' " ],
    "Full-Wave-Rectifier" : [['Vin', 'R' , 'C', 'F'], "Units: Vin = V ,  R = Ohm , C = mF , F = Hz, Diode = '1N4148' " ],
    "Low-Pass-RC-Filter" : [['Vin', 'R' , 'C'], "Units: Vin = V ,  R = kOhm , C = uF "],
    "High-Pass-RC-Filter" : [['Vin', 'R' , 'C'], "Units: Vin = V ,  R = kOhm , C = uF " ],
    "Series-Negative-Clipper": [['Vin', 'R', 'F'], "Units: Vin = V , R = Ohm , F = Hz, Diode = '1N4148' "],
    "Series-Positive-Clipper": [['Vin', 'R', 'F'], "Units: Vin = V , R = Ohm , F = Hz, Diode = '1N4148' "],
    "Positive-Clamper" :  [['Vin', 'R' , 'C', 'F'], "Units: Vin = V ,  R = Ohm , C = mF , F = Hz, Diode = '1N4148' " ],
    "Negative-Clamper" :  [['Vin', 'R' , 'C', 'F'], "Units: Vin = V ,  R = Ohm , C = mF , F = Hz, Diode = '1N4148' " ],
    "n-MOSFET-Characteristics": [['Vd', 'Vg'], "Units: Vd = V , Vg = V "],
}

def renderInput(item):
    args = {}
    args['list'] = circuitList
    args['title'] = item
    imgUrl = circuitImgList.get(item)
    args['imgUrl'] = imgUrl
    inputs = inputList.get(item)
    args['inputs'] = inputs[0]
    args['msg'] = inputs[1]
    return args

@app.route("/", methods=["GET", "POST"])
def index():
    args = {}
    args['list'] = circuitList
    if request.args:
        raw_req = request.args
        item = raw_req['item']
        args = renderInput(item)
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
    
    if formData['title'] == "Low-Pass-RC-Filter":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = low_pass_rc_filter(formData['Vin'], formData['R'], formData['C'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} kOhm , C = {} mF'.format(formData['Vin'], formData['R'], formData['C']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)
    
    if formData['title'] == "High-Pass-RC-Filter":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = high_pass_rc_filter(formData['Vin'], formData['R'], formData['C'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} kOhm , C = {} mF'.format(formData['Vin'], formData['R'], formData['C']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)

    if formData['title'] == "Series-Negative-Clipper":
        print("1")
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = series_negative_clipper(formData['Vin'], formData['R'], formData['F'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} kOhm , f = {} Hz'.format(formData['Vin'], formData['R'], formData['F']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)
    
    if formData['title'] == "Series-Positive-Clipper":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = series_positive_clipper(formData['Vin'], formData['R'], formData['F'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} kOhm , C = {} Hz'.format(formData['Vin'], formData['R'], formData['F']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)
    
    if formData['title'] == "Positive-Clamper":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = positive_clamper(formData['Vin'], formData['R'], formData['C'], formData['F'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} kOhm , C = {} mF , F = {} Hz'.format(formData['Vin'], formData['R'], formData['C'], formData['F']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)

    if formData['title'] == "Negative-Clamper":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = negative_clamper(formData['Vin'], formData['R'], formData['C'], formData['F'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vin = {} V , R = {} kOhm , C = {} mF , F = {} Hz'.format(formData['Vin'], formData['R'], formData['C'], formData['F']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)

    
    if formData['title'] == "n-MOSFET-Characteristics":
        args = {}
        args['list'] = circuitList
        args['imgUrl'] = formData['imgUrl']
        circuit, analysis, plot = nmos_characteristics(formData['Vd'], formData['Vg'])
        args['title'] = circuit.title
        buf = BytesIO()
        plot.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        args['plot'] = data
        inputs = str('Inputs: Vd = {} V , Vg = {} V'.format(formData['Vd'], formData['Vg']))
        args['inputs'] = inputs
        return render_template("output.html", args=args)


    return render_template("output.html", args=args)    

