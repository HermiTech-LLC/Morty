import os
import logging
from skidl import Part, Net, ERC
from lxml import etree

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to find library path dynamically using environment variables
def find_lib_path():
    paths = [
        os.getenv('KICAD6_3DMODEL_DIR', "/usr/share/kicad/3dmodels"),
        os.getenv('KICAD6_3RD_PARTY', "/home/loq1/.local/share/kicad/6.0/3rdparty"),
        os.getenv('KICAD6_FOOTPRINT_DIR', "/usr/share/kicad/footprints"),
        os.getenv('KICAD6_SYMBOL_DIR', "/usr/share/kicad/symbols"),
        os.getenv('KICAD6_TEMPLATE_DIR', "/usr/share/kicad/template"),
        os.getenv('KICAD_USER_TEMPLATE_DIR', "/home/loq1/.local/share/kicad/6.0/template"),
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

# Add component using SKiDL
def add_component(ref, value, footprint, x, y):
    try:
        component = Part('device', value, footprint=footprint, ref=ref)
        component.place(x, y)
        logging.info(f"Component {ref} added at ({x}, {y}).")
        return component
    except Exception as e:
        logging.error(f"Error adding component {ref}: {e}")
        raise

# Create a net and connect components using SKiDL
def create_and_connect_net(net_name, connections):
    try:
        net = Net(net_name)
        for conn in connections:
            net += conn
        logging.info(f"Net {net_name} created with connections: {connections}")
        return net
    except Exception as e:
        logging.error(f"Error creating net {net_name}: {e}")
        raise

# Add decoupling capacitors using SKiDL
def add_decoupling_caps(component, pin_name, gnd, num_caps=2):
    try:
        for i in range(num_caps):
            cap_ref = f"C_{component.ref}_{pin_name}_{i}"
            cap = Part('device', 'C', footprint="Capacitor_SMD", ref=cap_ref)
            cap[1] += component[pin_name]
            cap[2] += gnd
            logging.info(f"Decoupling capacitor {cap_ref} added.")
    except Exception as e:
        logging.error(f"Error adding decoupling capacitors for {component.ref}: {e}")
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
        netlist_content = "\n".join(f"{net.name} {' '.join(f'{c.ref}/{p}' for c, p in net.get_pins())}" for net in netlist)
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

    component_refs = {}
    for ref, value, footprint, x, y in components:
        component = add_component(ref, value, footprint, x, y)
        component_refs[ref] = component
        create_symbol_file(ref, project_directory)

    # Define power supply nets and connect components
    power_nets = {
        'VCC': [
            component_refs['U1'][1], component_refs['U2'][1], component_refs['U3'][1], component_refs['U4'][1],
            component_refs['U10'][1], component_refs['U12'][1], component_refs['U15'][1], component_refs['U17'][1],
            component_refs['U19'][1]
        ],
        'GND': [
            component_refs['U1'][2], component_refs['U2'][2], component_refs['U3'][2], component_refs['U4'][2],
            component_refs['U10'][2], component_refs['U12'][2], component_refs['U15'][2], component_refs['U17'][2],
            component_refs['U19'][2]
        ]
    }

    for net_name, connections in power_nets.items():
        create_and_connect_net(net_name, connections)

    # Connect decoupling capacitors
    decoupling_components = [
        'U1', 'U2', 'U3', 'U12', 'U15', 'U17', 'U19', 'U4'
    ]
    for component_ref in decoupling_components:
        component = component_refs[component_ref]
        add_decoupling_caps(component, 'VCC', component_refs['U10'][2])

    # Save the KiCad project file
    save_kicad_schematic(tree, schematic_file_path)

    # Create netlist
    netlist = [
        Net('VCC'), Net('GND')
    ]

    create_netlist_file(netlist, netlist_file_path)

    # Perform ERC
    ERC()

if __name__ == "__main__":
    main()