import os
import logging
from pyspice.logging.logging import setup_logging
from pyspice.probe import raw_probe
from pyspice.spice.netlist import Circuit, SubCircuitFactory
from pyspice.unit import *
from pyspice.spice.library import SpiceLibrary
from pyspice.simulation import Simulation, TransientAnalysis

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
setup_logging()

# Define the ESP32 SubCircuit
class ESP32(SubCircuitFactory):
    __name__ = 'ESP32'
    __nodes__ = ('VCC', 'GND', 'GPIO1', 'GPIO3', 'GPIO21', 'GPIO22', 'GPIO0', 'GPIO2', 'GPIO15', 'GPIO13', 'GPIO12', 'GPIO14', 'GPIO27', 'GPIO25', 'GPIO26', 'GPIO16', 'GPIO17', 'GPIO18', 'GPIO19', 'GPIO23', 'GPIO4', 'GPIO5', 'GPIO6', 'GPIO7', 'GPIO8', 'GPIO9', 'GPIO10', 'GPIO11', 'GPIO32', 'GPIO33', 'GPIO34', 'GPIO35', 'GPIO36', 'GPIO39', 'GPIO20')

    def __init__(self):
        super().__init__()
        self.VCC = self.VCC()
        self.GND = self.GND()

# Define the circuit
def add_components(circuit):
    components = {
        "ESP32_1": circuit.subcircuit(ESP32()),
        "ESP32_2": circuit.subcircuit(ESP32()),
        "CPU": circuit.X('CPU', 'ATMEGA2560', 'VCC', 'GND'),
        "RAM": circuit.X('RAM', 'MT48LC16M16A2P-75', 'VCC', 'GND'),
        "FLASH": circuit.X('FLASH', 'W25Q64FVSSIG', 'VCC', 'GND'),
        "UART": circuit.X('UART', 'MAX232', 'VCC', 'GND'),
        "PMIC": circuit.X('PMIC', 'TPS65217', 'VCC', 'GND'),
        "USB": circuit.X('USB', 'USB3320C-EZK', 'VCC', 'GND'),
        "ETH": circuit.X('ETH', 'LAN8720', 'VCC', 'GND'),
        "Clock": circuit.X('Clock', 'SI5351A-B-GT', 'VCC', 'GND'),
        "TPU": circuit.X('TPU', 'Edge_TPU', 'VCC', 'GND'),
        "FPGA": circuit.X('FPGA', 'XC7A35T-1FTG256C', 'VCC', 'GND'),
        "SDCard": circuit.X('SDCard', 'SD_Memory_Card_Mini_Micro_SD', 'VCC', 'GND'),
        "IMU": circuit.X('IMU', 'MPU6050', 'VCC', 'GND'),
        "Accelerometer": circuit.X('Accelerometer', 'ADXL345', 'VCC', 'GND'),
        "Gyro_PID": circuit.X('Gyro_PID', 'PID_Gyroscope', 'VCC', 'GND'),
        "Serial_Bus_Driver": circuit.X('Serial_Bus_Driver', 'MCP23017', 'VCC', 'GND')
    }
    logging.info("Components added to the schematic.")
    return components

def create_nets(circuit, components):
    vcc = circuit.V('VCC', 'VCC', circuit.gnd, 3.3@u_V)
    gnd = circuit.gnd

    power_pins = {
        'ESP32_1': ['VCC', 'GND'],
        'ESP32_2': ['VCC', 'GND'],
        'CPU': ['VCC', 'GND'],
        'RAM': ['VCC', 'GND'],
        'FLASH': ['VCC', 'GND'],
        'UART': ['VCC', 'GND'],
        'PMIC': ['VCC', 'GND'],
        'USB': ['VCC', 'GND'],
        'ETH': ['VCC', 'GND'],
        'Clock': ['VCC', 'GND'],
        'TPU': ['VCC', 'GND'],
        'FPGA': ['VCC', 'GND'],
        'SDCard': ['VCC', 'GND'],
        'IMU': ['VCC', 'GND'],
        'Accelerometer': ['VCC', 'GND'],
        'Gyro_PID': ['VCC', 'GND'],
        'Serial_Bus_Driver': ['VCC', 'GND']
    }

    for comp, pins in power_pins.items():
        circuit.X(comp, ESP32(), 'VCC', 'GND')

    logging.info("Power nets created and connected to components.")
    return vcc, gnd

def add_decoupling_caps(circuit, components, gnd):
    for comp in components:
        for i in range(2):  # Add two decoupling caps per component
            circuit.C(f'C_{comp}_{i}', 'VCC', gnd, 0.1@u_F)
            logging.info(f"Decoupling capacitor added to component {comp}.")
def connect_components(circuit, components):
    esp32_1 = components['ESP32_1']
    esp32_2 = components['ESP32_2']
    uart = components['UART']
    usb = components['USB']
    eth = components['ETH']
    clock = components['Clock']
    tpu = components['TPU']
    fpga = components['FPGA']
    sdcard = components['SDCard']
    imu = components['IMU']
    accelerometer = components['Accelerometer']
    gyro_pid = components['Gyro_PID']
    serial_bus_driver = components['Serial_Bus_Driver']
    ram = components['RAM']
    cpu = components['CPU']

    # Example connections
    circuit.R('R1', esp32_1.GPIO1, uart.T1IN, 1@u_kΩ)
    circuit.R('R2', esp32_1.GPIO3, uart.R1OUT, 1@u_kΩ)

    circuit.R('R3', esp32_2.GPIO1, uart.T2IN, 1@u_kΩ)
    circuit.R('R4', esp32_2.GPIO3, uart.R2OUT, 1@u_kΩ)

    circuit.R('R5', esp32_1.GPIO21, usb.DP, 1@u_kΩ)
    circuit.R('R6', esp32_1.GPIO22, usb.DM, 1@u_kΩ)

    circuit.R('R7', esp32_2.GPIO21, usb.DP, 1@u_kΩ)
    circuit.R('R8', esp32_2.GPIO22, usb.DM, 1@u_kΩ)

    circuit.R('R9', esp32_1.GPIO0, eth.TXEN, 1@u_kΩ)
    circuit.R('R10', esp32_1.GPIO2, eth.TXD0, 1@u_kΩ)

    circuit.R('R11', esp32_2.GPIO0, eth.TXEN, 1@u_kΩ)
    circuit.R('R12', esp32_2.GPIO2, eth.TXD0, 1@u_kΩ)

    circuit.R('R13', esp32_1.GPIO16, clock.CLK0, 1@u_kΩ)
    circuit.R('R14', esp32_1.GPIO17, clock.CLK1, 1@u_kΩ)

    circuit.R('R15', esp32_2.GPIO16, clock.CLK0, 1@u_kΩ)
    circuit.R('R16', esp32_2.GPIO17, clock.CLK1, 1@u_kΩ)

    circuit.R('R17', esp32_1.GPIO19, tpu.I2C_SDA, 1@u_kΩ)
    circuit.R('R18', esp32_1.GPIO23, tpu.I2C_SCL, 1@u_kΩ)

    circuit.R('R19', esp32_2.GPIO19, tpu.I2C_SDA, 1@u_kΩ)
    circuit.R('R20', esp32_2.GPIO23, tpu.I2C_SCL, 1@u_kΩ)

    circuit.R('R21', esp32_1.GPIO4, fpga.IO0, 1@u_kΩ)
    circuit.R('R22', esp32_1.GPIO5, fpga.IO1, 1@u_kΩ)

    circuit.R('R23', esp32_2.GPIO4, fpga.IO0, 1@u_kΩ)
    circuit.R('R24', esp32_2.GPIO5, fpga.IO1, 1@u_kΩ)

    circuit.R('R25', esp32_1.GPIO5, sdcard.CS, 1@u_kΩ)
    circuit.R('R26', esp32_1.GPIO18, sdcard.CLK, 1@u_kΩ)

    circuit.R('R27', esp32_2.GPIO5, sdcard.CS, 1@u_kΩ)
    circuit.R('R28', esp32_2.GPIO18, sdcard.CLK, 1@u_kΩ)

    circuit.R('R29', esp32_1.GPIO32, imu.SCL, 1@u_kΩ)
    circuit.R('R30', esp32_1.GPIO33, imu.SDA, 1@u_kΩ)

    circuit.R('R31', esp32_2.GPIO32, imu.SCL, 1@u_kΩ)
    circuit.R('R32', esp32_2.GPIO33, imu.SDA, 1@u_kΩ)

    circuit.R('R33', esp32_1.GPIO25, accelerometer.SCL, 1@u_kΩ)
    circuit.R('R34', esp32_1.GPIO26, accelerometer.SDA, 1@u_kΩ)

    circuit.R('R35', esp32_2.GPIO25, accelerometer.SCL, 1@u_kΩ)
    circuit.R('R36', esp32_2.GPIO26, accelerometer.SDA, 1@u_kΩ)

    circuit.R('R37', esp32_1.GPIO14, gyro_pid.IN, 1@u_kΩ)
    circuit.R('R38', esp32_1.GPIO15, gyro_pid.OUT, 1@u_kΩ)

    circuit.R('R39', esp32_2.GPIO14, gyro_pid.IN, 1@u_kΩ)
    circuit.R('R40', esp32_2.GPIO15, gyro_pid.OUT, 1@u_kΩ)

    circuit.R('R41', esp32_1.GPIO19, serial_bus_driver.SDA, 1@u_kΩ)
    circuit.R('R42', esp32_1.GPIO23, serial_bus_driver.SCL, 1@u_kΩ)

    circuit.R('R43', esp32_2.GPIO19, serial_bus_driver.SDA, 1@u_kΩ)
    circuit.R('R44', esp32_2.GPIO23, serial_bus_driver.SCL, 1@u_kΩ)

    # CPU to RAM
    for i in range(16):
        circuit.R(f'R{i+45}', cpu[f'AD{i}'], ram[f'DQ{i}'], 1@u_kΩ)
    for i in range(13):
        circuit.R(f'R{i+61}', cpu[f'A{i}'], ram[f'A{i}'], 1@u_kΩ)

    logging.info("Components connected.")

def save_netlist(circuit, file_path):
    circuit.write(file_path)
    logging.info(f"Netlist saved to {file_path}")

def main():
    project_directory = "Morty_project"
    os.makedirs(project_directory, exist_ok=True)
    netlist_file_path = os.path.join(project_directory, "morty_project.net")

    try:
        circuit = Circuit('Morty Project')
        components = add_components(circuit)
        vcc, gnd = create_nets(circuit, components)
        add_decoupling_caps(circuit, components, gnd)
        connect_components(circuit, components)
        save_netlist(circuit, netlist_file_path)

    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()