from app.circuits.OpAmps.OperationalAmplifier import BasicOperationalAmplifier
import numpy as np
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


# 1-voltage divider
# 2- current divider
# 3 - lCoscillaotr 
# 4- clipper 
# 5- clamper
# 6 - emiiter/CE amplifier
# 7-  cs amplifier
# 8 - voltage doubler
# 9 - half wave rectifier 
# 10 - voltage regulator

def operational_amplifier():
    circuit = Circuit('Operational Amplifier')
    # AC 1 PWL(0US 0V  0.01US 1V)
    circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=10000000@u_V)
    circuit.subcircuit(BasicOperationalAmplifier())
    circuit.X('op', 'BasicOperationalAmplifier', 'in', circuit.gnd, 'out')
    circuit.R('load', 'out', circuit.gnd, 470@u_Ω)
    circuit.R('R1','in','out', )

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
    
    return circuit, analysis, plt

def voltage_divider():
    circuit = Circuit('Voltage Divider')
    circuit.V('input', 1, circuit.gnd, 10@u_V)
    circuit.R(1, 1, 2, 2@u_kΩ)
    circuit.R(2, 2, circuit.gnd, 1@u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()
    output = {}
    for node in analysis.nodes.values():
        print('Node {}: {:5.2f} V'.format(str(node), float(node))
        output['Node {}'.format(str(node))] = {':5.2f'}.format(float(node))
    print(output)     