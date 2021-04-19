from app import app
from flask import render_template, request, redirect, jsonify
import numpy as np
import base64
from io import BytesIO
from circuit import operational_amplifier, voltage_divider

@app.route("/")
def index():
    voltage_divider()
    circuit, analysis, plt = operational_amplifier()
    print(circuit.title)
    for i in analysis.frequency:
        print(i)
    print(20*np.log10(np.absolute(analysis.out)))
    plt.show(block=True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("index.html", data=data, title=circuit.title)
