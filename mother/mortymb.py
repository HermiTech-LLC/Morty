import os
import pcbflow as pcb

# Define the board dimensions
board = pcb.Board((100, 80), name="MortyProject")  # Board size: 100mm x 80mm

# Add components to the board
components = {
    "ESP32_1": pcb.Component("ESP32-WROOM-32", (20, 20), footprint="ESP32-WROOM-32"),
    "ESP32_2": pcb.Component("ESP32-WROOM-32", (60, 20), footprint="ESP32-WROOM-32"),
    "CPU": pcb.Component("ATmega2560", (40, 40), footprint="TQFP-100"),
    "RAM": pcb.Component("MT48LC16M16A2P-75", (40, 60), footprint="TSOP-II-54"),
    "FLASH": pcb.Component("W25Q64FVSSIG", (70, 60), footprint="SOIC-8"),
    "UART": pcb.Component("MAX232", (10, 60), footprint="SOIC-16"),
    "PMIC": pcb.Component("TPS65217", (10, 40), footprint="QFN-48"),
    "USB": pcb.Component("USB3320C-EZK", (80, 20), footprint="QFN-24"),
    "ETH": pcb.Component("LAN8720", (80, 40), footprint="QFN-32"),
    "Clock": pcb.Component("SI5351A-B-GT", (80, 60), footprint="QFN-20"),
    "TPU": pcb.Component("Edge_TPU", (20, 60), footprint="BGA-256"),
    "FPGA": pcb.Component("XC7A35T-1FTG256C", (60, 60), footprint="BGA-256"),
    "SDCard": pcb.Component("SD_Card_Socket", (20, 80), footprint="SD_Card"),
    "IMU": pcb.Component("MPU6050", (60, 80), footprint="QFN-24"),
    "Accelerometer": pcb.Component("ADXL345", (40, 20), footprint="LGA-14"),
    "Gyro_PID": pcb.Component("PID_Gyroscope", (10, 80), footprint="DIP-16"),
    "Serial_Bus_Driver": pcb.Component("MCP23017", (70, 80), footprint="SSOP-28"),
}

# Add components to the board
for name, component in components.items():
    board.add(component)

# Create power and ground nets
vcc = pcb.Net("VCC")
gnd = pcb.Net("GND")

# Connect power and ground pins
power_pins = ['VCC', 'GND']
for component in components.values():
    for pin_name in power_pins:
        try:
            pin = component.get_pin(pin_name)
            if pin_name == 'VCC':
                vcc.connect(pin)
            elif pin_name == 'GND':
                gnd.connect(pin)
        except KeyError:
            pass

# Example connections (full set of connections based on provided script)
try:
    # UART connections
    components["UART"].connect("T1IN", components["ESP32_1"].get_pin("GPIO1"))
    components["UART"].connect("R1OUT", components["ESP32_1"].get_pin("GPIO3"))
    components["UART"].connect("T2IN", components["ESP32_2"].get_pin("GPIO1"))
    components["UART"].connect("R2OUT", components["ESP32_2"].get_pin("GPIO3"))
    # USB connections
    components["USB"].connect("DP", components["ESP32_1"].get_pin("GPIO21"))
    components["USB"].connect("DM", components["ESP32_1"].get_pin("GPIO22"))
    components["USB"].connect("DP", components["ESP32_2"].get_pin("GPIO21"))
    components["USB"].connect("DM", components["ESP32_2"].get_pin("GPIO22"))
    # Ethernet connections
    eth_pins = ["TXEN", "TXD0", "TXD1", "RXER", "RXD0", "RXD1", "CRS", "MDC", "MDIO"]
    esp_pins_1 = ["GPIO0", "GPIO2", "GPIO15", "GPIO13", "GPIO12", "GPIO14", "GPIO27", "GPIO25", "GPIO26"]
    esp_pins_2 = ["GPIO0", "GPIO2", "GPIO15", "GPIO13", "GPIO12", "GPIO14", "GPIO27", "GPIO25", "GPIO26"]
    for eth_pin, esp_pin_1, esp_pin_2 in zip(eth_pins, esp_pins_1, esp_pins_2):
        components["ETH"].connect(eth_pin, components["ESP32_1"].get_pin(esp_pin_1))
        components["ETH"].connect(eth_pin, components["ESP32_2"].get_pin(esp_pin_2))

    # Clock connections
    components["Clock"].connect("CLK0", components["ESP32_1"].get_pin("GPIO16"))
    components["Clock"].connect("CLK1", components["ESP32_1"].get_pin("GPIO17"))
    components["Clock"].connect("CLK2", components["ESP32_1"].get_pin("GPIO18"))
    components["Clock"].connect("CLK0", components["ESP32_2"].get_pin("GPIO16"))
    components["Clock"].connect("CLK1", components["ESP32_2"].get_pin("GPIO17"))
    components["Clock"].connect("CLK2", components["ESP32_2"].get_pin("GPIO18"))
        # TPU connections
    components["TPU"].connect("I2C_SDA", components["ESP32_1"].get_pin("GPIO19"))
    components["TPU"].connect("I2C_SCL", components["ESP32_1"].get_pin("GPIO23"))
    components["TPU"].connect("I2C_SDA", components["ESP32_2"].get_pin("GPIO19"))
    components["TPU"].connect("I2C_SCL", components["ESP32_2"].get_pin("GPIO23"))

    # FPGA connections
    fpga_pins = ["IO0", "IO1", "IO2", "IO3", "IO4", "IO5", "IO6", "IO7", "IO8", "IO9", "IO10", "IO11", "IO12", "IO13"]
    esp_fpga_pins = ["GPIO4", "GPIO5", "GPIO6", "GPIO7", "GPIO8", "GPIO9", "GPIO10", "GPIO11", "GPIO32", "GPIO33", "GPIO34", "GPIO35", "GPIO36", "GPIO39"]
    for fpga_pin, esp_pin in zip(fpga_pins, esp_fpga_pins):
        components["FPGA"].connect(fpga_pin, components["ESP32_1"].get_pin(esp_pin))
        components["FPGA"].connect(fpga_pin, components["ESP32_2"].get_pin(esp_pin))

    # SDCard connections
    components["SDCard"].connect("CS", components["ESP32_1"].get_pin("GPIO5"))
    components["SDCard"].connect("CLK", components["ESP32_1"].get_pin("GPIO18"))
    components["SDCard"].connect("CMD", components["ESP32_1"].get_pin("GPIO19"))
    components["SDCard"].connect("D0", components["ESP32_1"].get_pin("GPIO23"))
    components["SDCard"].connect("D1", components["ESP32_1"].get_pin("GPIO22"))
    components["SDCard"].connect("D2", components["ESP32_1"].get_pin("GPIO21"))
    components["SDCard"].connect("D3", components["ESP32_1"].get_pin("GPIO20"))

    components["SDCard"].connect("CS", components["ESP32_2"].get_pin("GPIO5"))
    components["SDCard"].connect("CLK", components["ESP32_2"].get_pin("GPIO18"))
    components["SDCard"].connect("CMD", components["ESP32_2"].get_pin("GPIO19"))
    components["SDCard"].connect("D0", components["ESP32_2"].get_pin("GPIO23"))
    components["SDCard"].connect("D1", components["ESP32_2"].get_pin("GPIO22"))
    components["SDCard"].connect("D2", components["ESP32_2"].get_pin("GPIO21"))
    components["SDCard"].connect("D3", components["ESP32_2"].get_pin("GPIO20"))

    # IMU connections
    components["IMU"].connect("SCL", components["ESP32_1"].get_pin("GPIO32"))
    components["IMU"].connect("SDA", components["ESP32_1"].get_pin("GPIO33"))
    components["IMU"].connect("SCL", components["ESP32_2"].get_pin("GPIO32"))
    components["IMU"].connect("SDA", components["ESP32_2"].get_pin("GPIO33"))

    # Accelerometer connections
    components["Accelerometer"].connect("SCL", components["ESP32_1"].get_pin("GPIO25"))
    components["Accelerometer"].connect("SDA", components["ESP32_1"].get_pin("GPIO26"))
    components["Accelerometer"].connect("SCL", components["ESP32_2"].get_pin("GPIO25"))
    components["Accelerometer"].connect("SDA", components["ESP32_2"].get_pin("GPIO26"))

    # Gyro PID connections
    components["Gyro_PID"].connect("IN", components["ESP32_1"].get_pin("GPIO14"))
    components["Gyro_PID"].connect("OUT", components["ESP32_1"].get_pin("GPIO15"))
    components["Gyro_PID"].connect("IN", components["ESP32_2"].get_pin("GPIO14"))
    components["Gyro_PID"].connect("OUT", components["ESP32_2"].get_pin("GPIO15"))

    # Serial Bus Driver connections
    components["Serial_Bus_Driver"].connect("SDA", components["ESP32_1"].get_pin("GPIO19"))
    components["Serial_Bus_Driver"].connect("SCL", components["ESP32_1"].get_pin("GPIO23"))
    components["Serial_Bus_Driver"].connect("SDA", components["ESP32_2"].get_pin("GPIO19"))
    components["Serial_Bus_Driver"].connect("SCL", components["ESP32_2"].get_pin("GPIO23"))

    # CPU to RAM connections
    ram_pins = ["DQ0", "DQ1", "DQ2", "DQ3", "DQ4", "DQ5", "DQ6", "DQ7", "DQ8", "DQ9", "DQ10", "DQ11", "DQ12", "DQ13", "DQ14", "DQ15", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12"]
    cpu_pins = ["AD0", "AD1", "AD2", "AD3", "AD4", "AD5", "AD6", "AD7", "AD8", "AD9", "AD10", "AD11", "AD12", "AD13", "AD14", "AD15", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12"]
    for ram_pin, cpu_pin in zip(ram_pins, cpu_pins):
        components["RAM"].connect(ram_pin, components["CPU"].get_pin(cpu_pin))

except KeyError as e:
    print(f"Error connecting components: {e}")

# Add decoupling capacitors
def add_decoupling_caps(component):
    vcc_pins = [pin for pin in component.pins if 'VCC' in pin.name]
    for pin in vcc_pins:
        cap = pcb.Component("C", (0, 0), footprint="0805", value="0.1uF")
        board.add(cap)
        vcc.connect(cap.get_pin(1))
        gnd.connect(cap.get_pin(2))
        vcc.connect(pin)

for component in components.values():
    add_decoupling_caps(component)

# Save the board design to files
output_directory = "MortyProject"
os.makedirs(output_directory, exist_ok=True)
board.save(os.path.join(output_directory, "MortyProject.kicad_pcb"))

print("PCB design saved to MortyProject.kicad_pcb")

# Generate Gerber files
board.generate_gerbers(output_directory)
print(f"Gerber files generated in {output_directory}")