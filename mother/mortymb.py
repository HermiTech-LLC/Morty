import os
import logging
from skidl import Part, Net, ERC, generate_netlist
from skidl.libs.xess.lib import res, cap, ind, opamp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define components and add them to the schematic
def add_components():
    components = {
        "ESP32_1": Part('MCU_Module', 'ESP32-WROOM-32', footprint='ESP32-WROOM-32'),
        "ESP32_2": Part('MCU_Module', 'ESP32-WROOM-32', footprint='ESP32-WROOM-32'),
        "CPU": Part('MCU_Microchip_ATmega', 'ATmega2560', footprint='TQFP-100'),
        "RAM": Part('Memory_RAM', 'MT48LC16M16A2P-75', footprint='TSOP-II-54_8x22mm_P0.8mm'),
        "FLASH": Part('Memory_FLASH', 'W25Q64FVSSIG', footprint='SOIC-8_3.9x4.9mm_P1.27mm'),
        "UART": Part('Interface_UART', 'MAX232', footprint='SOIC-16_3.9x9.9mm_P1.27mm'),
        "PMIC": Part('Power_Management', 'TPS65217', footprint='QFN-48_7x7mm_P0.5mm'),
        "USB": Part('Interface_USB', 'USB3320C-EZK', footprint='QFN-24_4x4mm_P0.5mm'),
        "ETH": Part('Interface_Ethernet', 'LAN8720', footprint='QFN-32_5x5mm_P0.5mm'),
        "Clock": Part('Clock_Generator', 'SI5351A-B-GT', footprint='QFN-20_3x3mm_P0.5mm'),
        "TPU": Part('Google_TPU', 'Edge_TPU', footprint='BGA-256_17x17mm_P1.0mm'),
        "FPGA": Part('FPGA_Xilinx', 'XC7A35T-1FTG256C', footprint='BGA-256_17x17mm_P1.0mm'),
        "SDCard": Part('Memory_Card', 'SD_Card_Socket', footprint='SD_Memory_Card_Mini_Micro_SD'),
        "IMU": Part('Sensor_IMU', 'MPU6050', footprint='QFN-24_4x4mm_P0.5mm'),
        "Accelerometer": Part('Sensor_Accelerometer', 'ADXL345', footprint='LGA-14_3x5mm_P0.8mm'),
        "Gyro_PID": Part('Control_Module', 'PID_Gyroscope', footprint='DIP-16_3.9x19.3mm_P2.54mm'),
        "Serial_Bus_Driver": Part('Interface_Serial', 'MCP23017', footprint='SSOP-28_3.9x9.9mm_P0.635mm')
    }
    logging.info("Components added to the schematic.")
    return components

# Define power supply nets and connect components
def create_nets(components):
    vcc = Net('VCC')
    gnd = Net('GND')

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
        vcc += components[comp][pins[0]]
        gnd += components[comp][pins[1]]
    
    logging.info("Power nets created and connected to components.")
    return vcc, gnd

# Add decoupling capacitors
def add_decoupling_caps(components, gnd):
    for comp in components:
        vcc_pins = [pin.name for pin in components[comp].pins if 'VCC' in pin.name]
        for pin in vcc_pins:
            for i in range(2):  # Add two decoupling caps per VCC pin
                capacitor = Part('Device', 'C', value='0.1uF', footprint='Capacitor_SMD:C_0805')
                capacitor[1] += components[comp][pin]
                capacitor[2] += gnd
                logging.info(f"Decoupling capacitor added to component {comp}.")

# Connect components
def connect_components(components):
    esp32_1 = components['ESP32_1']
    esp32_2 = components['ESP32_2']
    cpu = components['CPU']
    ram = components['RAM']
    flash = components['FLASH']
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
    
    # Example connections
    # ESP32_1 to UART
    esp32_1['GPIO1'] += uart['T1IN']
    esp32_1['GPIO3'] += uart['R1OUT']

    # ESP32_2 to UART
    esp32_2['GPIO1'] += uart['T2IN']
    esp32_2['GPIO3'] += uart['R2OUT']

    # ESP32_1 to USB
    esp32_1['GPIO21'] += usb['DP']
    esp32_1['GPIO22'] += usb['DM']

    # ESP32_2 to USB
    esp32_2['GPIO21'] += usb['DP']
    esp32_2['GPIO22'] += usb['DM']

    # ESP32_1 to Ethernet
    esp32_1['GPIO0'] += eth['TXEN']
    esp32_1['GPIO2'] += eth['TXD0']
    esp32_1['GPIO15'] += eth['TXD1']
    esp32_1['GPIO13'] += eth['RXER']
    esp32_1['GPIO12'] += eth['RXD0']
    esp32_1['GPIO14'] += eth['RXD1']
    esp32_1['GPIO27'] += eth['CRS']
    esp32_1['GPIO25'] += eth['MDC']
    esp32_1['GPIO26'] += eth['MDIO']

    # ESP32_2 to Ethernet
    esp32_2['GPIO0'] += eth['TXEN']
    esp32_2['GPIO2'] += eth['TXD0']
    esp32_2['GPIO15'] += eth['TXD1']
    esp32_2['GPIO13'] += eth['RXER']
    esp32_2['GPIO12'] += eth['RXD0']
    esp32_2['GPIO14'] += eth['RXD1']
    esp32_2['GPIO27'] += eth['CRS']
    esp32_2['GPIO25'] += eth['MDC']
    esp32_2['GPIO26'] += eth['MDIO']

    # ESP32_1 to Clock
    esp32_1['GPIO16'] += clock['CLK0']
    esp32_1['GPIO17'] += clock['CLK1']
    esp32_1['GPIO18'] += clock['CLK2']

    # ESP32_2 to Clock
    esp32_2['GPIO16'] += clock['CLK0']
    esp32_2['GPIO17'] += clock['CLK1']
    esp32_2['GPIO18'] += clock['CLK2']

    # ESP32_1 to TPU
    esp32_1['GPIO19'] += tpu['I2C_SDA']
    esp32_1['GPIO23'] += tpu['I2C_SCL']

    # ESP32_2 to TPU
    esp32_2['GPIO19'] += tpu['I2C_SDA']
    esp32_2['GPIO23'] += tpu['I2C_SCL']

    # ESP32_1 to FPGA
    esp32_1['GPIO4'] += fpga['IO0']
    esp32_1['GPIO5'] += fpga['IO1']
    esp32_1['GPIO6'] += fpga['IO2']
    esp32_1['GPIO7'] += fpga['IO3']
    esp32_1['GPIO8'] += fpga['IO4']
    esp32_1['GPIO9'] += fpga['IO5']
    esp32_1['GPIO10'] += fpga['IO6']
    esp32_1['GPIO11'] += fpga['IO7']
    esp32_1['GPIO32'] += fpga['IO8']
    esp32_1['GPIO33'] += fpga['IO9']
    esp32_1['GPIO34'] += fpga['IO10']
    esp32_1['GPIO35'] += fpga['IO11']
    esp32_1['GPIO36'] += fpga['IO12']
    esp32_1['GPIO39'] += fpga['IO13']

    # ESP32_2 to FPGA
    esp32_2['GPIO4'] += fpga['IO0']
    esp32_2['GPIO5'] += fpga['IO1']
    esp32_2['GPIO6'] += fpga['IO2']
    esp32_2['GPIO7'] += fpga['IO3']
    esp32_2['GPIO8'] += fpga['IO4']
    esp32_2['GPIO9'] += fpga['IO5']
    esp32_2['GPIO10'] += fpga['IO6']
    esp32_2['GPIO11'] += fpga['IO7']
    esp32_2['GPIO32'] += fpga['IO8']
    esp32_2['GPIO33'] += fpga['IO9']
    esp32_2['GPIO34'] += fpga['IO10']
    esp32_2['GPIO35'] += fpga['IO11']
    esp32_2['GPIO36'] += fpga['IO12']
    esp32_2['GPIO39'] += fpga['IO13']

    # CPU to RAM
    cpu['AD0'] += ram['DQ0']
    cpu['AD1'] += ram['DQ1']
    cpu['AD2'] += ram['DQ2']
    cpu['AD3'] += ram['DQ3']
    cpu['AD4'] += ram['DQ4']
    cpu['AD5'] += ram['DQ5']
    cpu['AD6'] += ram['DQ6']
    cpu['AD7'] += ram['DQ7']
    cpu['AD8'] += ram['DQ8']
    cpu['AD9'] += ram['DQ9']
    cpu['AD10'] += ram['DQ10']
    cpu['AD11'] += ram['DQ11']
    cpu['AD12'] += ram['DQ12']
    cpu['AD13'] += ram['DQ13']
    cpu['AD14'] += ram['DQ14']
    cpu['AD15'] += ram['DQ15']
    cpu['A0'] += ram['A0']
    cpu['A1'] += ram['A1']
    cpu['A2'] += ram['A2']
    cpu['A3'] += ram['A3']
    cpu['A4'] += ram['A4']
    cpu['A5'] += ram['A5']
    cpu['A6'] += ram['A6']
    cpu['A7'] += ram['A7']
    cpu['A8'] += ram['A8']
    cpu['A9'] += ram['A9']
    cpu['A10'] += ram['A10']
    cpu['A11'] += ram['A11']
    cpu['A12'] += ram['A12']

    # ESP32_1 to SDCard
    esp32_1['GPIO5'] += sdcard['CS']
    esp32_1['GPIO18'] += sdcard['CLK']
    esp32_1['GPIO19'] += sdcard['CMD']
    esp32_1['GPIO23'] += sdcard['D0']
    esp32_1['GPIO22'] += sdcard['D1']
    esp32_1['GPIO21'] += sdcard['D2']
    esp32_1['GPIO20'] += sdcard['D3']

    # ESP32_2 to SDCard
    esp32_2['GPIO5'] += sdcard['CS']
    esp32_2['GPIO18'] += sdcard['CLK']
    esp32_2['GPIO19'] += sdcard['CMD']
    esp32_2['GPIO23'] += sdcard['D0']
    esp32_2['GPIO22'] += sdcard['D1']
    esp32_2['GPIO21'] += sdcard['D2']
    esp32_2['GPIO20'] += sdcard['D3']

    # ESP32_1 to IMU
    esp32_1['GPIO32'] += imu['SCL']
    esp32_1['GPIO33'] += imu['SDA']

    # ESP32_2 to IMU
    esp32_2['GPIO32'] += imu['SCL']
    esp32_2['GPIO33'] += imu['SDA']

    # ESP32_1 to Accelerometer
    esp32_1['GPIO25'] += accelerometer['SCL']
    esp32_1['GPIO26'] += accelerometer['SDA']

    # ESP32_2 to Accelerometer
    esp32_2['GPIO25'] += accelerometer['SCL']
    esp32_2['GPIO26'] += accelerometer['SDA']

    # ESP32_1 to Gyro PID
    esp32_1['GPIO14'] += gyro_pid['IN']
    esp32_1['GPIO15'] += gyro_pid['OUT']

    # ESP32_2 to Gyro PID
    esp32_2['GPIO14'] += gyro_pid['IN']
    esp32_2['GPIO15'] += gyro_pid['OUT']

    # ESP32_1 to Serial Bus Driver
    esp32_1['GPIO19'] += serial_bus_driver['SDA']
    esp32_1['GPIO23'] += serial_bus_driver['SCL']

    # ESP32_2 to Serial Bus Driver
    esp32_2['GPIO19'] += serial_bus_driver['SDA']
    esp32_2['GPIO23'] += serial_bus_driver['SCL']

    logging.info("Components connected.")

# Save netlist to file
def save_netlist(file_path):
    generate_netlist(file_=file_path)
    logging.info(f"Netlist saved to {file_path}")

# Save PCB design to file
def save_pcb(file_path):
    from skidl.pcb import pcb
    pcb.save(file_path)
    logging.info(f"PCB design saved to {file_path}")

def main():
    project_directory = "Morty_project"
    os.makedirs(project_directory, exist_ok=True)
    netlist_file_path = os.path.join(project_directory, "morty_project.net")
    pcb_file_path = os.path.join(project_directory, "morty_project.kicad_pcb")

    try:
        components = add_components()
        vcc, gnd = create_nets(components)
        add_decoupling_caps(components, gnd)
        connect_components(components)
        save_netlist(netlist_file_path)
        save_pcb(pcb_file_path)

        # Perform ERC
        ERC()
        logging.info("ERC completed successfully.")
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()