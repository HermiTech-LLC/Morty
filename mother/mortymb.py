import os
from lxml import etree

# Function to find gEDA library path dynamically
def find_geda_lib_path():
    geda_paths = [
        "/usr/share/gEDA/sym",
        os.path.expanduser("~/.gEDA/sym"),
    ]
    for path in geda_paths:
        if os.path.exists(path):
            return path
    return None

geda_symbol_dir = find_geda_lib_path()
if not geda_symbol_dir:
    print("ERROR: gEDA library path not found.")
    exit(1)

def load_geda_file(file_path):
    try:
        tree = etree.parse(file_path)
        return tree
    except Exception as e:
        print(f"Error loading gEDA file: {e}")
        return None

def save_geda_file(tree, file_path):
    try:
        with open(file_path, 'wb') as file:
            tree.write(file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"File saved successfully: {file_path}")
    except Exception as e:
        print(f"Error saving gEDA file: {e}")

def add_component(tree, component_name, x, y):
    root = tree.getroot()
    components = root.find(".//components")
    if components is None:
        components = etree.Element("components")
        root.append(components)

    new_component = etree.Element("component")
    new_component.set("name", component_name)
    new_component.set("x", str(x))
    new_component.set("y", str(y))
    components.append(new_component)
    print(f"Component {component_name} added at ({x}, {y}).")

def create_net(name):
    net = etree.Element("net")
    net.set("name", name)
    return net

def connect_components(tree, net, component_pins):
    for component, pin in component_pins:
        connection = etree.Element("connection")
        connection.set("component", component)
        connection.set("pin", pin)
        net.append(connection)
    root = tree.getroot()
    nets = root.find(".//nets")
    if nets is None:
        nets = etree.Element("nets")
        root.append(nets)
    nets.append(net)
    print(f"Net {net.get('name')} created with connections: {component_pins}")

def add_decoupling_caps(tree, component_name, pin_name, gnd, num_caps=2):
    caps = []
    for i in range(num_caps):
        cap_name = f"C_{component_name}_{pin_name}_{i}"
        add_component(tree, cap_name, 0, 0)  # Placeholder coordinates
        caps.append((cap_name, '1'))  # Assuming '1' is the power pin of the capacitor
        connect_components(tree, create_net(cap_name), [(cap_name, '1'), (component_name, pin_name), (cap_name, '2'), (gnd, '')])
    return caps

def main():
    file_path = "your_geda_project.sch"
    tree = load_geda_file(file_path)
    if tree is None:
        return

    # Define components and add them to the schematic
    components = [
        ("cpu", 10, 20),
        ("ram1", 30, 20),
        ("ram2", 50, 20),
        ("fpga", 70, 20),
        ("uart_comm", 90, 20),
        ("pcie_slot1", 110, 20),
        ("pcie_slot2", 130, 20),
        ("gpu1", 150, 20),
        ("gpu2", 170, 20),
        ("pmic", 190, 20),
        ("atx_power", 210, 20),
        ("usb_ctrl", 230, 20),
        ("usb_port1", 250, 20),
        ("usb_port2", 270, 20),
        ("eth_ctrl", 290, 20),
        ("eth_port", 310, 20),
        ("sata_ctrl", 330, 20),
        ("sata_port1", 350, 20),
        ("clock_gen", 370, 20),
    ]

    for component, x, y in components:
        add_component(tree, component, x, y)

    # Define power supply nets
    power_nets = {
        'VCC': create_net('VCC'),
        'GND': create_net('GND'),
        'PCIE_VCC': create_net('PCIE_VCC'),
        'PCIE_GND': create_net('PCIE_GND'),
        'USB_VCC': create_net('USB_VCC'),
        'ETH_VCC': create_net('ETH_VCC'),
        'SATA_VCC': create_net('SATA_VCC'),
        'FPGA_VCC': create_net('FPGA_VCC'),
        'FPGA_GND': create_net('FPGA_GND')
    }

    # Connect power and ground to components
    connect_components(tree, power_nets['VCC'], [
        ('cpu', 'VCC'), ('ram1', 'VCC'), ('ram2', 'VCC'), ('fpga', 'VCC'),
        ('pmic', 'VCC'), ('usb_ctrl', 'VCC'), ('eth_ctrl', 'VCC'), ('sata_ctrl', 'VCC'),
        ('clock_gen', 'VCC')
    ])
    connect_components(tree, power_nets['GND'], [
        ('cpu', 'GND'), ('ram1', 'GND'), ('ram2', 'GND'), ('fpga', 'GND'),
        ('pmic', 'GND'), ('usb_ctrl', 'GND'), ('eth_ctrl', 'GND'), ('sata_ctrl', 'GND'),
        ('clock_gen', 'GND')
    ])

    # Connect decoupling capacitors
    add_decoupling_caps(tree, 'cpu', 'VCC', 'GND')
    add_decoupling_caps(tree, 'ram1', 'VCC', 'GND')
    add_decoupling_caps(tree, 'ram2', 'VCC', 'GND')
    add_decoupling_caps(tree, 'usb_ctrl', 'VCC', 'GND')
    add_decoupling_caps(tree, 'eth_ctrl', 'VCC', 'GND')
    add_decoupling_caps(tree, 'sata_ctrl', 'VCC', 'GND')
    add_decoupling_caps(tree, 'clock_gen', 'VCC', 'GND')
    add_decoupling_caps(tree, 'fpga', 'VCC', 'GND')

    # Save the modified gEDA project file
    save_geda_file(tree, "modified_geda_project.sch")

if __name__ == "__main__":
    main()