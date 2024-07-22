import os
from lxml import etree

# Function to find library path dynamically (originally for gEDA, adapted for this script)
def find_lib_path():
    paths = [
        "/usr/share/gEDA/sym",
        os.path.expanduser("~/.gEDA/sym"),
        "/usr/share/kicad/library",
        os.path.expanduser("~/.kicad/library"),
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

# Create a new KiCad schematic file
def create_kicad_schematic():
    root = etree.Element("kicad_sch")
    version = etree.SubElement(root, "version")
    version.text = "20211014"

    paper = etree.SubElement(root, "paper")
    paper.text = "A4"

    return etree.ElementTree(root)

# Save KiCad schematic file
def save_kicad_schematic(tree, file_path):
    try:
        with open(file_path, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"File saved successfully: {file_path}")
    except Exception as e:
        print(f"Error saving KiCad schematic file: {e}")

# Add component to the schematic
def add_component(tree, ref, value, footprint, x, y):
    root = tree.getroot()
    components = root.find(".//components")
    if components is None:
        components = etree.Element("components")
        root.append(components)

    component = etree.Element("comp")
    component.set("ref", ref)

    value_element = etree.Element("value")
    value_element.text = value
    component.append(value_element)

    footprint_element = etree.Element("footprint")
    footprint_element.text = footprint
    component.append(footprint_element)

    placement = etree.Element("placement")
    placement.set("x", str(x))
    placement.set("y", str(y))
    component.append(placement)

    components.append(component)
    print(f"Component {ref} added at ({x}, {y}).")

# Create a net and connect components
def create_and_connect_net(tree, net_name, connections):
    root = tree.getroot()
    nets = root.find(".//nets")
    if nets is None:
        nets = etree.Element("nets")
        root.append(nets)

    net = etree.Element("net")
    net.set("name", net_name)

    for conn in connections:
        node = etree.Element("node")
        node.set("ref", conn[0])
        node.set("pin", conn[1])
        net.append(node)

    nets.append(net)
    print(f"Net {net_name} created with connections: {connections}")

# Add decoupling capacitors
def add_decoupling_caps(tree, component_ref, pin_name, gnd, num_caps=2):
    caps = []
    for i in range(num_caps):
        cap_ref = f"C_{component_ref}_{pin_name}_{i}"
        add_component(tree, cap_ref, "C", "Capacitor_SMD", 0, 0)  # Placeholder coordinates
        caps.append((cap_ref, '1'))  # Assuming '1' is the power pin of the capacitor
        create_and_connect_net(tree, cap_ref, [(cap_ref, '1'), (component_ref, pin_name), (cap_ref, '2'), (gnd, '')])
    return caps

# Create a symbol file for the component (from gEDA)
def create_symbol_file(component_name, directory):
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
    print(f"Symbol file created: {symbol_file_path}")

# Create a netlist file (from gEDA)
def create_netlist_file(netlist, file_path):
    netlist_content = "\n".join(f"{net['name']} {' '.join(f'{c}/{p}' for c, p in net['connections'])}" for net in netlist)
    with open(file_path, 'w') as f:
        f.write(netlist_content)
    print(f"Netlist file created: {file_path}")
def main():
    project_directory = "kicad_project"
    os.makedirs(project_directory, exist_ok=True)
    schematic_file_path = os.path.join(project_directory, "morty.sch")
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