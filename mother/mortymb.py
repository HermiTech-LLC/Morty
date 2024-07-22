import os
import logging
from lxml import etree

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to find library path dynamically
def find_lib_path():
    paths = [
        "/usr/share/gEDA/sym",
        os.path.expanduser("~/.gEDA/sym"),
        "/usr/share/kicad/library",
        os.path.expanduser("~/.kicad/library"),
    ]
    for path in paths:
        if os.path.exists(path):
            logging.info(f"Library path found: {path}")
            return path
    logging.warning("Library path not found")
    return None

# Create a new KiCad schematic file
def create_kicad_schematic():
    try:
        root = etree.Element("kicad_sch", version="20200310")
        etree.SubElement(root, "host", tool="eeschema", version="(5.99.0-1467-g4b4952b09)")
        etree.SubElement(root, "page").text = "A3"

        title_block = etree.SubElement(root, "title_block")
        etree.SubElement(title_block, "title").text = "Morty Project"
        etree.SubElement(title_block, "company").text = "HermiTech"
        etree.SubElement(title_block, "rev").text = "1"

        etree.SubElement(root, "lib_symbols")
        etree.SubElement(root, "nets")

        logging.info("KiCad schematic structure created successfully")
        return etree.ElementTree(root)
    except Exception as e:
        logging.error(f"Error creating KiCad schematic: {e}")
        raise

# Save KiCad schematic file
def save_kicad_schematic(tree, file_path):
    try:
        with open(file_path, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        logging.info(f"File saved successfully: {file_path}")
    except Exception as e:
        logging.error(f"Error saving KiCad schematic file: {e}")
        raise

# Add component to the schematic
def add_component(tree, ref, value, footprint, x, y):
    try:
        root = tree.getroot()
        lib_symbols = root.find(".//lib_symbols")
        symbol = etree.SubElement(lib_symbols, "symbol", ref=ref)
        etree.SubElement(symbol, "value").text = value
        etree.SubElement(symbol, "footprint").text = footprint
        etree.SubElement(symbol, "at", x=str(x), y=str(y))
        etree.SubElement(symbol, "uuid").text = os.urandom(16).hex()
        logging.info(f"Component {ref} added at ({x}, {y}).")
    except Exception as e:
        logging.error(f"Error adding component {ref}: {e}")
        raise

# Create a net and connect components
def create_and_connect_net(tree, net_name, connections):
    try:
        root = tree.getroot()
        nets = root.find(".//nets")
        net = etree.SubElement(nets, "net", name=net_name)
        for conn in connections:
            node = etree.SubElement(net, "node", ref=conn[0], pin=conn[1])
        logging.info(f"Net {net_name} created with connections: {connections}")
    except Exception as e:
        logging.error(f"Error creating net {net_name}: {e}")
        raise

# Add decoupling capacitors
def add_decoupling_caps(tree, component_ref, pin_name, gnd, num_caps=2):
    try:
        for i in range(num_caps):
            cap_ref = f"C_{component_ref}_{pin_name}_{i}"
            add_component(tree, cap_ref, "C", "Capacitor_SMD", 0, 0)
            create_and_connect_net(tree, cap_ref, [(cap_ref, '1'), (component_ref, pin_name), (cap_ref, '2'), (gnd, '')])
    except Exception as e:
        logging.error(f"Error adding decoupling capacitors for {component_ref}: {e}")
        raise
# Create a symbol file for the component
def create_symbol_file(component_name, directory):
    try:
        symbol_file_path = os.path.join(directory, f"{component_name}.sym")
        symbol_content = f"""v 20210605 1
C {component_name}
{{
    T 0 0 5 10 1 1 0 0 1
    T 0 0 5 10 1 1 0 0 1
    L 0 0 100 100
}}
"""
        with open(symbol_file_path, 'w') as f:
            f.write(symbol_content)
        logging.info(f"Symbol file created: {symbol_file_path}")
    except Exception as e:
        logging.error(f"Error creating symbol file for {component_name}: {e}")
        raise

# Create a netlist file
def create_netlist_file(netlist, file_path):
    try:
        netlist_content = "\n".join(f"{net['name']} {' '.join(f'{c}/{p}' for c, p in net['connections'])}" for net in netlist)
        with open(file_path, 'w') as f:
            f.write(netlist_content)
        logging.info(f"Netlist file created: {file_path}")
    except Exception as e:
        logging.error(f"Error creating netlist file: {e}")
        raise

def main():
    project_directory = "kicad_project"
    os.makedirs(project_directory, exist_ok=True)
    schematic_file_path = os.path.join(project_directory, "morty.kicad_sch")
    netlist_file_path = os.path.join(project_directory, "morty.net")

    tree = create_kicad_schematic()

    # Define components and add them to the schematic
    components = [
        ("U1", "CPU", "CPU_Footprint", 20, 50),
        ("U2", "RAM1", "RAM_Footprint", 40, 60),
        ("U3", "RAM2", "RAM_Footprint", 60, 60),
        ("U4", "FPGA", "FPGA_Footprint", 50, 50),
        ("U5", "UART_Comm", "UART_Footprint", 70, 40),
        ("U6", "PCIe_Slot1", "PCIe_Footprint", 30, 80),
        ("U7", "PCIe_Slot2", "PCIe_Footprint", 40, 80),
        ("U8", "GPU1", "GPU_Footprint", 35, 90),
        ("U9", "GPU2", "GPU_Footprint", 45, 90),
        ("U10", "PMIC", "PMIC_Footprint", 10, 40),
        ("U11", "ATX_Power", "Power_Footprint", 10, 30),
        ("U12", "USB_Ctrl", "USB_Footprint", 70, 30),
        ("U13", "USB_Port1", "USB_Port_Footprint", 80, 20),
        ("U14", "USB_Port2", "USB_Port_Footprint", 90, 20),
        ("U15", "ETH_Ctrl", "ETH_Footprint", 80, 50),
        ("U16", "ETH_Port", "ETH_Port_Footprint", 90, 50),
        ("U17", "SATA_Ctrl", "SATA_Footprint", 50, 20),
        ("U18", "SATA_Port1", "SATA_Port_Footprint", 55, 10),
        ("U19", "Clock_Gen", "Clock_Footprint", 45, 20),
    ]

    for ref, value, footprint, x, y in components:
        add_component(tree, ref, value, footprint, x, y)
        create_symbol_file(ref, project_directory)

    # Define power supply nets and connect components
    power_nets = {
        'VCC': [
            ('U1', 'VCC'), ('U2', 'VCC'), ('U3', 'VCC'), ('U4', 'VCC'),
            ('U10', 'VCC'), ('U12', 'VCC'), ('U15', 'VCC'), ('U17', 'VCC'),
            ('U19', 'VCC')
        ],
        'GND': [
            ('U1', 'GND'), ('U2', 'GND'), ('U3', 'GND'), ('U4', 'GND'),
            ('U10', 'GND'), ('U12', 'GND'), ('U15', 'GND'), ('U17', 'GND'),
            ('U19', 'GND')
        ]
    }

    for net_name, connections in power_nets.items():
        create_and_connect_net(tree, net_name, connections)

    # Connect decoupling capacitors
    decoupling_components = [
        'U1', 'U2', 'U3', 'U12', 'U15', 'U17', 'U19', 'U4'
    ]
    for component in decoupling_components:
        add_decoupling_caps(tree, component, 'VCC', 'GND')

    # Save the KiCad project file
    save_kicad_schematic(tree, schematic_file_path)

    # Create netlist
    netlist = [
        {'name': 'VCC', 'connections': [('U1', 'VCC'), ('U2', 'VCC'), ('U3', 'VCC'), ('U4', 'VCC'), ('U10', 'VCC'), ('U12', 'VCC'), ('U15', 'VCC'), ('U17', 'VCC'), ('U19', 'VCC')]},
        {'name': 'GND', 'connections': [('U1', 'GND'), ('U2', 'GND'), ('U3', 'GND'), ('U4', 'GND'), ('U10', 'GND'), ('U12', 'GND'), ('U15', 'GND'), ('U17', 'GND'), ('U19', 'GND')]}
    ]
    
    create_netlist_file(netlist, netlist_file_path)

if __name__ == "__main__":
    main()