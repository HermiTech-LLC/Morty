import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Git repositories for KiCad libraries
LIBRARIES = {
    "ESP32-WROOM-32": "https://github.com/espressif/kicad-libraries.git",
    "ATMEGA": "https://github.com/KiCad/kicad-symbols.git",
    "MICRON": "https://github.com/KiCad/kicad-footprints.git",
    "WINBOND": "https://github.com/KiCad/kicad-footprints.git",
    "MAXIM": "https://github.com/KiCad/kicad-symbols.git",
    "TI": "https://github.com/KiCad/kicad-footprints.git",
    "MICROCHIP": "https://github.com/KiCad/kicad-symbols.git",
    "LAN8720": "https://github.com/KiCad/kicad-footprints.git",
    "SI5351A": "https://github.com/KiCad/kicad-symbols.git",
    "GOOGLE_EDGE_TPU": "https://github.com/KiCad/kicad-footprints.git",
    "XILINX": "https://github.com/KiCad/kicad-footprints.git",
    "GENERIC": "https://github.com/KiCad/kicad-footprints.git",
    "TDK": "https://github.com/KiCad/kicad-symbols.git",
    "ANALOG_DEVICES": "https://github.com/KiCad/kicad-symbols.git"
}

# Directory to store downloaded libraries
LIB_DIR = os.path.expanduser("~/kicad_libraries")

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        logging.info(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute: {command}")
        raise e

def clone_or_update_repo(repo_url, dest_dir):
    if os.path.exists(dest_dir):
        logging.info(f"Updating existing repository at {dest_dir}")
        run_command(f"cd {dest_dir} && git pull")
    else:
        logging.info(f"Cloning repository from {repo_url} to {dest_dir}")
        run_command(f"git clone {repo_url} {dest_dir}")

def ensure_libraries_installed():
    if not os.path.exists(LIB_DIR):
        os.makedirs(LIB_DIR)

    for lib_name, repo_url in LIBRARIES.items():
        dest_dir = os.path.join(LIB_DIR, lib_name)
        clone_or_update_repo(repo_url, dest_dir)

    sym_lib_table_path = os.path.expanduser("~/.config/kicad/sym-lib-table")
    fp_lib_table_path = os.path.expanduser("~/.config/kicad/fp-lib-table")

    with open(sym_lib_table_path, 'a') as sym_file, open(fp_lib_table_path, 'a') as fp_file:
        for lib_name in LIBRARIES.keys():
            sym_file.write(f"(lib (name {lib_name})(type KiCad)(uri \"{os.path.join(LIB_DIR, lib_name)}\")(options \"\")(descr \"\"))\n")
            fp_file.write(f"(lib (name {lib_name})(type KiCad)(uri \"{os.path.join(LIB_DIR, lib_name)}\")(options \"\")(descr \"\"))\n")

def generate_schematic(file_path):
    logging.info(f"Generating schematic at {file_path}")
    with open(file_path, 'w') as sch_file:
        sch_file.write("EESchema Schematic File Version 4\n")
        sch_file.write("LIBS:Device\n")
        sch_file.write("EELAYER 25 0\n")
        sch_file.write("EELAYER END\n")
        sch_file.write("$Descr A4 11693 8268\n")
        sch_file.write("encoding utf-8\n")
        sch_file.write("Sheet 1 1\n")
        sch_file.write("Title \"Morty Project\"\n")
        sch_file.write("Date \"2024-07-28\"\n")
        sch_file.write("Rev \"1\"\n")
        sch_file.write("Comp \"\"\n")
        sch_file.write("Comment1 \"\"\n")
        sch_file.write("Comment2 \"\"\n")
        sch_file.write("Comment3 \"\"\n")
        sch_file.write("Comment4 \"\"\n")
        sch_file.write("$EndDescr\n")
        
        components = [
            ("ESP32", "U1", "ESP32-WROOM-32"),
            ("ATMEGA328P", "U2", "ATMEGA"),
            ("MT25QL128", "U3", "MICRON"),
            ("W25Q64", "U4", "WINBOND"),
            ("MAX232", "U5", "MAXIM"),
            ("LM1117", "U6", "TI"),
            ("PIC16F877A", "U7", "MICROCHIP"),
            ("LAN8720", "U8", "LAN8720"),
            ("SI5351A", "U9", "SI5351A"),
            ("GOOGLE-EDGE-TPU", "U10", "GOOGLE_EDGE_TPU"),
            ("XC7A35T", "U11", "XILINX"),
            ("GENERIC", "U12", "GENERIC"),
            ("TDK", "U13", "TDK"),
            ("ADXL345", "U14", "ANALOG_DEVICES")
        ]
        
        for comp, ref, lib in components:
            sch_file.write(f"$Comp\nL {lib}:{comp} {ref}\nU 1 1 5F7A3243\nP 300 200\nF 0 \"{ref}\" H 300 220 50  0000 C CNN\nF 1 \"\" H 300 180 50  0000 C CNN\nF 2 \"\" H 300 200 50  0001 C CNN\nF 3 \"\" H 300 200 50  0001 C CNN\n\t1    300 200\n\t1    0    0    -1\n$EndComp\n")
        
        sch_file.write("$EndSCHEMATIC\n")
    logging.info(f"Schematic file generated: {file_path}")

def generate_netlist(schematic_file_path, netlist_path):
    logging.info("Generating netlist from schematic")
    command = f"kicad-cli sch export netlist {schematic_file_path} -o {netlist_path}"
    run_command(command)
    logging.info(f"Netlist saved to {netlist_path}")

def generate_pcb(netlist_path, pcb_file_path):
    logging.info(f"Generating PCB from netlist at {pcb_file_path}")
    pcb_content = """
    (kicad_pcb (version 20210606) (generator pcbnew)
    (page A4)
    (title_block
        (title "Morty Project")
        (company "")
        (rev "")
        (date "2024-07-28")
        (comment 1 "")
        (comment 2 "")
        (comment 3 "")
        (comment 4 "")
    )
    (general
        (links 14)
        (no_connects 0)
        (area 0 0 210 297)
        (thickness 1.6)
        (drawings 2)
        (tracks 0)
        (zones 0)
        (modules 14)
        (nets 14)
    )
    (layers
        (0 F.Cu signal)
        (31 B.Cu signal)
        (32 B.Adhes user)
        (33 F.Adhes user)
        (34 B.Paste user)
        (35 F.Paste user)
        (36 B.SilkS user)
        (37 F.SilkS user)
        (38 B.Mask user)
        (39 F.Mask user)
        (40 Dwgs.User user)
        (41 Cmts.User user)
        (42 Eco1.User user)
        (43 Eco2.User user)
        (44 Edge.Cuts user)
        (45 Margin user)
        (46 B.CrtYd user)
        (47 F.CrtYd user)
        (48 B.Fab user)
        (49 F.Fab user)
    )
    (setup
        (last_trace_width 0.25)
        (trace_clearance 0.2)
        (zone_clearance 0.508)
        (zone_45_only no)
        (trace_min 0.2)
        (segment_width 0.2)
        (edge_width 0.05)
        (via_size 0.6)
        (via_drill 0.4)
        (via_min_size 0.4)
        (via_min_drill 0.3)
        (uvia_size 0.3)
        (uvia_drill 0.1)
        (uvias_allowed no)
        (uvia_min_size 0.2)
        (uvia_min_drill 0.1)
        (pcb_text_width 0.3)
        (pcb_text_size 1.5 1.5)
        (mod_edge_width 0.15)
        (mod_text_size 1 1)
        (mod_text_width 0.15)
        (pad_size 1.524 1.524)
        (pad_drill 0.762)
        (pad_to_mask_clearance 0.2)
        (solder_mask_min_width 0.1)
        (draw_clearance 0.2)
        (solder_mask_min_width 0.05)
        (mod_clearance 0.1)
        (mod_clearance_width 0.1)
        (mod_pad_to_mask_clearance 0.2)
        (mod_mask_margin 0.1)
        (mod_mask_min_width 0.1)
        (edge_clearance 0.01)
        (edge_45_clearance 0.05)
        (text_outside_min_clearance 0.2)
        (text_outside_pad_to_mask_clearance 0.2)
        (pad_clearance 0.2)
        (silk_top 0.12)
        (silk_bottom 0.12)
        (mask_top 0.12)
        (mask_bottom 0.12)
        (paste_top 0.12)
        (paste_bottom 0.12)
        (via_type normal)
        (thermal_gap 0.508)
        (thermal_bridge_width 0.508)
        (zone_clearance 0.508)
        (zone_45_only yes)
    )
    (net 0 "")
    (net 1 "/NetU1-1")
    (net 2 "/NetU2-1")
    (net 3 "/NetU3-1")
    (net 4 "/NetU4-1")
    (net 5 "/NetU5-1")
    (net 6 "/NetU6-1")
    (net 7 "/NetU7-1")
    (net 8 "/NetU8-1")
    (net 9 "/NetU9-1")
    (net 10 "/NetU10-1")
    (net 11 "/NetU11-1")
    (net 12 "/NetU12-1")
    (net 13 "/NetU13-1")
    (net 14 "/NetU14-1")
    (net_class Default "This is the default net class."
        (clearance 0.2)
        (trace_width 0.25)
        (via_dia 0.6)
        (via_drill 0.4)
        (uvia_dia 0.3)
        (uvia_drill 0.1)
    )
    (module ESP32-WROOM-32:ESP32 (layer F.Cu) (tedit 5F7A3243)
        (at 100 100)
        (path /5F7A3243)
        (fp_text reference U1 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value ESP32 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module ATMEGA:ATMEGA328P (layer F.Cu) (tedit 5F7A3244)
        (at 100 150)
        (path /5F7A3244)
        (fp_text reference U2 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value ATMEGA328P (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module MICRON:MT25QL128 (layer F.Cu) (tedit 5F7A3245)
        (at 100 200)
        (path /5F7A3245)
        (fp_text reference U3 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value MT25QL128 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module WINBOND:W25Q64 (layer F.Cu) (tedit 5F7A3246)
        (at 100 250)
        (path /5F7A3246)
        (fp_text reference U4 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value W25Q64 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module MAXIM:MAX232 (layer F.Cu) (tedit 5F7A3247)
        (at 100 300)
        (path /5F7A3247)
        (fp_text reference U5 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value MAX232 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module TI:LM1117 (layer F.Cu) (tedit 5F7A3248)
        (at 100 350)
        (path /5F7A3248)
        (fp_text reference U6 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value LM1117 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module MICROCHIP:PIC16F877A (layer F.Cu) (tedit 5F7A3249)
        (at 100 400)
        (path /5F7A3249)
        (fp_text reference U7 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value PIC16F877A (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module LAN8720:LAN8720 (layer F.Cu) (tedit 5F7A3250)
        (at 100 450)
        (path /5F7A3250)
        (fp_text reference U8 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value LAN8720 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module SI5351A:SI5351A (layer F.Cu) (tedit 5F7A3251)
        (at 100 500)
        (path /5F7A3251)
        (fp_text reference U9 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value SI5351A (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module GOOGLE_EDGE_TPU:GOOGLE-EDGE-TPU (layer F.Cu) (tedit 5F7A3252)
        (at 100 550)
        (path /5F7A3252)
        (fp_text reference U10 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value GOOGLE-EDGE-TPU (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module XILINX:XC7A35T (layer F.Cu) (tedit 5F7A3253)
        (at 100 600)
        (path /5F7A3253)
        (fp_text reference U11 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value XC7A35T (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module GENERIC:GENERIC (layer F.Cu) (tedit 5F7A3254)
        (at 100 650)
        (path /5F7A3254)
        (fp_text reference U12 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value GENERIC (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module TDK:TDK (layer F.Cu) (tedit 5F7A3255)
        (at 100 700)
        (path /5F7A3255)
        (fp_text reference U13 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value TDK (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    (module ANALOG_DEVICES:ADXL345 (layer F.Cu) (tedit 5F7A3256)
        (at 100 750)
        (path /5F7A3256)
        (fp_text reference U14 (at 0 0) (layer F.SilkS)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (fp_text value ADXL345 (at 0 -1.5) (layer F.Fab)
            (effects (font (size 1 1) (thickness 0.15)))
        )
        (pad 1 smd rect (at -1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
        (pad 2 smd rect (at 1 0) (size 1 1) (layers F.Cu F.Paste F.Mask))
    )
    )
    """
    with open(pcb_file_path, 'w') as pcb_file:
        pcb_file.write(pcb_content)
    command = f"kicad-cli pcb export step {pcb_file_path} -o {pcb_file_path.replace('.kicad_pcb', '.step')}"
    run_command(command)
    logging.info(f"PCB file generated: {pcb_file_path}")

def main():
    project_directory = "Morty_project"
    os.makedirs(project_directory, exist_ok=True)
    schematic_file_path = os.path.join(project_directory, "morty_project.kicad_sch")
    netlist_file_path = os.path.join(project_directory, "morty_project.net")
    pcb_file_path = os.path.join(project_directory, "morty_project.kicad_pcb")

    try:
        ensure_libraries_installed()
        generate_schematic(schematic_file_path)
        generate_netlist(schematic_file_path, netlist_file_path)
        generate_pcb(netlist_file_path, pcb_file_path)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()