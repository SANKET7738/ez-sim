from app.circuits.OpAmps.OperationalAmplifier import BasicOperationalAmplifier
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Physics.SemiConductor import ShockleyDiode

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

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

def voltage_divider(v,r1,r2):
    circuit = Circuit('Voltage Divider')
    circuit.V('input', 1, circuit.gnd, u_V(float(v)))
    circuit.R(1, 1, 2, u_kOhm(float(r1)))
    circuit.R(2, 2, circuit.gnd, u_kOhm(float(r2)))
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()
    output = {}
    for node in analysis.nodes.values():
        output[str(node)] = str(round(float(node),2)) + "V"  

    return circuit, analysis, output

def current_divider(i,r1,r2):
    circuit = Circuit('Current Divider')
    circuit.I('input', 1, circuit.gnd, u_A(float(i))) # Fixme: current value
    circuit.R(1, 1, circuit.gnd, u_kOhm(float(r1)))
    circuit.R(2, 1, circuit.gnd, u_kOhm(float(r2)))

    for resistance in (circuit.R1, circuit.R2):
        resistance.minus.add_current_probe(circuit) # to get positive value

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()
    output = {}
    for node in analysis.branches.values():
        output[str(node)] = str(round(float(node),2)) + "A" 

    return circuit, analysis, output

def diode_characteristic_curve(v,r):
    circuit = Circuit('Diode Characteristic Curve')
    circuit.include('./app/circuits/libraries/diode/switching/1N4148.lib')
    circuit.V('input', 'in', circuit.gnd, u_V(float(v)))
    circuit.R(1, 'in', 'out', u_Ohm(float(r))) # not required for simulation
    circuit.X('D1', '1N4148', 'out', circuit.gnd)
    #r# We simulate the circuit at these temperatures: 0, 25 and 100 °C.
    # Fixme: Xyce ???
    temperatures = [0, 25, 100]@u_Degree
    analyses = {}
    for temperature in temperatures:
        simulator = circuit.simulator(temperature=temperature, nominal_temperature=temperature)
        analysis = simulator.dc(Vinput=slice(-2, 5, .01))
        analyses[float(temperature)] = analysis
    silicon_forward_voltage_threshold = .7
    shockley_diode = ShockleyDiode(Is=4e-9, degree=25)

    def two_scales_tick_formatter(value, position):
        if value >= 0:
            return '{} mA'.format(value)
        else:
            return '{} nA'.format(value/100)
    formatter = ticker.FuncFormatter(two_scales_tick_formatter)

    figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))
    ax1.set_title('1N4148 Characteristic Curve ')
    ax1.set_xlabel('Voltage [V]')
    ax1.set_ylabel('Current')
    ax1.grid()
    ax1.set_xlim(-2, 2)
    ax1.axvspan(-2, 0, facecolor='green', alpha=.2)
    ax1.axvspan(0, silicon_forward_voltage_threshold, facecolor='blue', alpha=.1)
    ax1.axvspan(silicon_forward_voltage_threshold, 2, facecolor='blue', alpha=.2)
    ax1.set_ylim(-500, 750) # Fixme: round
    ax1.yaxis.set_major_formatter(formatter)
    Vd = analyses[25].out
    # compute scale for reverse and forward region
    forward_region = Vd >= 0@u_V
    reverse_region = np.invert(forward_region)
    scale =  reverse_region*1e11 + forward_region*1e3
    #?# check temperature
    for temperature in temperatures:
        analysis = analyses[float(temperature)]
        ax1.plot(Vd, - analysis.Vinput * scale)
    ax1.plot(Vd, shockley_diode.I(Vd) * scale, 'black')
    ax1.legend(['@ {} °C'.format(temperature)
                for temperature in temperatures] + ['Shockley Diode Model Is = 4 nA'],
            loc=(.02,.8))
    ax1.axvline(x=0, color='black')
    ax1.axhline(y=0, color='black')
    ax1.axvline(x=silicon_forward_voltage_threshold, color='red')
    ax1.text(-1, -100, 'Reverse Biased Region', ha='center', va='center')
    ax1.text( 1, -100, 'Forward Biased Region', ha='center', va='center')
    ax2.set_title('Resistance @ 25 °C')
    ax2.grid()
    ax2.set_xlim(-2, 3)
    ax2.axvspan(-2, 0, facecolor='green', alpha=.2)
    ax2.axvspan(0, silicon_forward_voltage_threshold, facecolor='blue', alpha=.1)
    ax2.axvspan(silicon_forward_voltage_threshold, 3, facecolor='blue', alpha=.2)
    analysis = analyses[25]
    static_resistance = -analysis.out / analysis.Vinput
    dynamic_resistance = np.diff(-analysis.out) / np.diff(analysis.Vinput)
    ax2.semilogy(analysis.out, static_resistance, base=10)
    ax2.semilogy(analysis.out[10:-1], dynamic_resistance[10:], base=10)
    ax2.axvline(x=0, color='black')
    ax2.axvline(x=silicon_forward_voltage_threshold, color='red')
    ax2.axhline(y=1, color='red')
    ax2.text(-1.5, 1.1, 'R limitation = 1 Ω', color='red')
    ax2.legend(['{} Resistance'.format(x) for x in ('Static', 'Dynamic')], loc=(.05,.2))
    ax2.set_xlabel('Voltage [V]')
    ax2.set_ylabel('Resistance [Ω]')

    return circuit, analysis, plt 

def half_wave_rectifier(v,r,c,f):
    circuit = Circuit('half-wave rectification')
    circuit.include('./app/circuits/libraries/diode/switching/1N4148.lib')
    source = circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=u_V(float(v)), frequency=u_Hz(float(f)))
    circuit.X('D1', '1N4148', 'in', 'output')
    circuit.R('load', 'output', circuit.gnd, u_Ω(float(r)))

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)
    figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

    ax1.set_title('Half-Wave Rectification')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Voltage [V]')
    ax1.grid()
    ax1.plot(analysis['in'])
    ax1.plot(analysis.output)
    ax1.legend(('input', 'output'), loc=(.05,.1))
    ax1.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

    circuit.C('1', 'output', circuit.gnd, u_mF(float(c)))

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

    ax2.set_title('Half-Wave Rectification with filtering')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Voltage [V]')
    ax2.grid()
    ax2.plot(analysis['in'])
    ax2.plot(analysis.output)
    ax2.legend(('input', 'output'), loc=(.05,.1))
    ax2.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))
    plt.tight_layout()

    return circuit, analysis, plt
     
def full_wave_rectifier(v,r,c,f):
    circuit = Circuit('Full-wave rectification')
    circuit.include('./app/circuits/libraries/diode/switching/1N4148.lib')
    source = circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=u_V(float(v)), frequency=u_Hz(float(f)))
    circuit.X('D1', '1N4148', 'in', 'output_plus')
    circuit.R('load', 'output_plus', 'output_minus', u_Ω(float(r)))
    circuit.X('D2', '1N4148', 'output_minus', circuit.gnd)
    circuit.X('D3', '1N4148', circuit.gnd, 'output_plus')
    circuit.X('D4', '1N4148', 'output_minus', 'in')

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)
    figure, (ax3, ax4) = plt.subplots(2, figsize=(20, 10))

    ax3.set_title('Full-Wave Rectification')
    ax3.set_xlabel('Time [s]')
    ax3.set_ylabel('Voltage [V]')
    ax3.grid()
    ax3.plot(analysis['in'])
    ax3.plot(analysis.output_plus - analysis.output_minus)
    ax3.legend(('input', 'output'), loc=(.05,.1))
    ax3.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

    circuit.C('1', 'output_plus', 'output_minus', u_mF(float(c)))

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

    ax4.set_title('Full-Wave Rectification with filtering')
    ax4.set_xlabel('Time [s]')
    ax4.set_ylabel('Voltage [V]')
    ax4.grid()
    ax4.plot(analysis['in'])
    ax4.plot(analysis.output_plus - analysis.output_minus)
    ax4.legend(('input', 'output'), loc=(.05,.1))
    ax4.set_ylim(float(-source.amplitude*1.1), float(source.amplitude*1.1))

    plt.tight_layout()

    return circuit, analysis, plt
