from app import app
from flask import render_template, request, redirect, jsonify
from app.circuits.OpAmps.OperationalAmplifier import BasicOperationalAmplifier
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

@app.route("/")
def index():
    circuit = Circuit('Operational Amplifier')
    # AC 1 PWL(0US 0V  0.01US 1V)
    circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=1@u_V)
    circuit.subcircuit(BasicOperationalAmplifier())
    circuit.X('op', 'BasicOperationalAmplifier', 'in', circuit.gnd, 'out')
    circuit.R('load', 'out', circuit.gnd, 470@u_Ω)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=1@u_Hz, stop_frequency=100@u_MHz, number_of_points=5,  variation='dec')

    figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

    plt.title("Bode Diagram of an Operational Amplifier")
    bode_diagram(axes=(ax1, ax2),
                frequency=analysis.frequency,
                gain=20*np.log10(np.absolute(analysis.out)),
                phase=np.angle(analysis.out, deg=False),
                marker='.',
                color='blue',
                linestyle='-',
                )
    print(0)
    plt.tight_layout()
    print(1)
    print(plt)
    plt.show(block=True)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("index.html", data=data)
