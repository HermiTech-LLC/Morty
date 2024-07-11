from skidl import *

# Define power supply nets
power_nets = {
    'VCC': Net('VCC'),
    'GND': Net('GND'),
    'PCIE_VCC': Net('PCIE_VCC'),
    'PCIE_GND': Net('PCIE_GND'),
    'USB_VCC': Net('USB_VCC'),
    'ETH_VCC': Net('ETH_VCC'),
    'SATA_VCC': Net('SATA_VCC'),
    'FPGA_VCC': Net('FPGA_VCC'),
    'FPGA_GND': Net('FPGA_GND')
}

# Helper function to add decoupling capacitors
def add_decoupling_caps(part, pin_name, gnd, num_caps=2):
    caps = []
    for _ in range(num_caps):
        cap = Part('device', 'C', value='100nF', footprint='0603')
        cap[1] += part[pin_name]
        cap[2] += gnd
        caps.append(cap)
    return caps

# Define components
cpu = Part('amd', 'Ryzen9_7950X', footprint='AM5')
ram = [Part('memory', 'DDR4', footprint='DIMM-288') for _ in range(2)]
fpga = Part('xilinx', 'Spartan6', footprint='BGA-256')
uart_comm = Part('my_lib', 'uart_comm')
pcie_slots = [Part('connector', 'PCIE_SLOT', footprint='PCIEX16') for _ in range(6)]
gpus = [Part('amd', 'RadeonRX', footprint='BGA-256') for _ in range(6)]
pmic = Part('ti', 'TPS65217', footprint='QFN-32')
atx_power = Part('connector', 'ATX_POWER', footprint='ATX-24')
usb_ctrl = Part('nec', 'D720200', footprint='QFN-64')
usb_ports = [Part('connector', 'USB_PORT', footprint='USB-A') for _ in range(4)]
eth_ctrl = Part('realtek', 'RTL8111', footprint='QFN-64')
eth_port = Part('connector', 'ETHERNET_PORT', footprint='RJ45')
sata_ctrl = Part('marvell', '88SE9215', footprint='QFN-64')
sata_ports = [Part('connector', 'SATA_PORT', footprint='SATA') for _ in range(4)]
clock_gen = Part('idt', '5V9885', footprint='QFN-32')
vrms = {net: Part('ti', 'TPS7A4501', footprint='DPAK') for net in power_nets.keys() if net != 'GND'}

# Connect power and ground
for net in power_nets.values():
    net.drive = POWER

# Connect CPU power and ground
power_nets['VCC'] += cpu['VCC']
power_nets['GND'] += cpu['GND']

# Connect RAM
for r in ram:
    power_nets['VCC'] += r['VCC']
    power_nets['GND'] += r['GND']
    cpu['ADDR0', 'ADDR1', 'ADDR2', 'ADDR3', 'ADDR4', 'ADDR5', 'ADDR6', 'ADDR7'] += r['ADDR0', 'ADDR1', 'ADDR2', 'ADDR3', 'ADDR4', 'ADDR5', 'ADDR6', 'ADDR7']
    cpu['DATA0', 'DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA5', 'DATA6', 'DATA7'] += r['DATA0', 'DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA5', 'DATA6', 'DATA7']

# Connect FPGA
power_nets['FPGA_VCC'] += fpga['VCC']
power_nets['FPGA_GND'] += fpga['GND']

# Connect UART
cpu['UART_TX'] += uart_comm['uart_rx']
uart_comm['uart_tx'] += fpga['UART_RX']
fpga['UART_TX'] += uart_comm['uart_rx']
uart_comm['uart_tx'] += cpu['UART_RX']

# Connect PCIe slots and GPUs
for i, (pcie_slot, gpu) in enumerate(zip(pcie_slots, gpus)):
    power_nets['PCIE_VCC'] += pcie_slot['VCC'], gpu['PCIE_VCC']
    power_nets['PCIE_GND'] += pcie_slot['GND'], gpu['PCIE_GND']
    cpu[f'PCIE_TX{i}'] += gpu['PCIE_RX']
    gpu['PCIE_TX'] += cpu[f'PCIE_RX{i}']
    pcie_slot['TX'] += gpu['PCIE_TX']
    gpu['PCIE_RX'] += pcie_slot['RX']

# Connect PMIC
power_nets['VCC'] += pmic['VCC']
power_nets['GND'] += pmic['GND']
pmic['OUT1'] += cpu['VCC']
pmic['OUT2'] += [ram[0]['VCC'], ram[1]['VCC'], power_nets['PCIE_VCC']]
atx_power['12V'] += pmic['IN']

# Connect USB Controller and Ports
power_nets['VCC'] += usb_ctrl['VCC']
power_nets['GND'] += usb_ctrl['GND']
cpu['USB_TX', 'USB_RX'] += usb_ctrl['TX', 'RX']
for i, usb_port in enumerate(usb_ports):
    power_nets['USB_VCC'] += usb_port['VCC']
    power_nets['GND'] += usb_port['GND']
    usb_port['D+'] += usb_ctrl[f'D+{i}']
    usb_port['D-'] += usb_ctrl[f'D-{i}']

# Connect Ethernet Controller and Port
power_nets['VCC'] += eth_ctrl['VCC']
power_nets['GND'] += eth_ctrl['GND']
cpu['ETH_TX', 'ETH_RX'] += eth_ctrl['TX', 'RX']
power_nets['ETH_VCC'] += eth_port['VCC']
power_nets['GND'] += eth_port['GND']
eth_port['TX+'] += eth_ctrl['TX+']
eth_port['TX-'] += eth_ctrl['TX-']
eth_port['RX+'] += eth_ctrl['RX+']
eth_port['RX-'] += eth_ctrl['RX-']

# Connect SATA Controller and Ports
power_nets['VCC'] += sata_ctrl['VCC']
power_nets['GND'] += sata_ctrl['GND']
cpu['SATA_TX', 'SATA_RX'] += sata_ctrl['TX', 'RX']
for i, sata_port in enumerate(sata_ports):
    power_nets['SATA_VCC'] += sata_port['VCC']
    power_nets['GND'] += sata_port['GND']
    sata_port['TX+'] += sata_ctrl[f'TX+{i}']
    sata_port['TX-'] += sata_ctrl[f'TX-{i}']
    sata_port['RX+'] += sata_ctrl[f'RX+{i}']
    sata_port['RX-'] += sata_ctrl[f'RX-{i}']

# Connect Clock Generator
power_nets['VCC'] += clock_gen['VCC']
power_nets['GND'] += clock_gen['GND']
clock_gen['CLK_OUT'] += cpu['CLK']

# Connect VRMs
for net, vrm in vrms.items():
    if net == 'USB_VCC':
        vrm['IN'] += atx_power['5V']
    else:
        vrm['IN'] += atx_power['12V']
    vrm['OUT'] += power_nets[net]

# Add decoupling capacitors
add_decoupling_caps(cpu, 'VCC', power_nets['GND'])
add_decoupling_caps(ram[0], 'VCC', power_nets['GND'])
add_decoupling_caps(ram[1], 'VCC', power_nets['GND'])
add_decoupling_caps(usb_ctrl, 'VCC', power_nets['GND'])
add_decoupling_caps(eth_ctrl, 'VCC', power_nets['GND'])
add_decoupling_caps(sata_ctrl, 'VCC', power_nets['GND'])
add_decoupling_caps(clock_gen, 'VCC', power_nets['GND'])
add_decoupling_caps(fpga, 'VCC', power_nets['GND'])

# Generate the netlist
try:
    generate_netlist()
    output_file = 'complete_advanced_motherboard.net'
    generate_netlist(output_file)
    generate_schematic(output_file.replace('.net', '.sch'))
    generate_pcb(output_file.replace('.net', '.kicad_pcb'))
    print("Netlist, schematic, and PCB layout generated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Instructions to run the script:
# 1. Ensure you have SKiDL installed: `pip install skidl`
# 2. Save this script as `motherboard_design.py`.
# 3. Run the script using: `python motherboard_design.py`.
# 4. Open the generated files in KiCad to verify the design.
