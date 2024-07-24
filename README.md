# Bipedal Humanoid Control System

___
![img](https://github.com/HermiTech-LLC/Morty/blob/main/Images/Mort.jpg)
___

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Dependencies](#dependencies)
- [Setup](#setup)
  - [Install Dependencies](#install-dependencies)
  - [Compile the Verilog Modules](#compile-the-verilog-modules)
  - [Run the ROS Node](#run-the-ros-node)
  - [Automate the Process](#automate-the-process)
- [Usage](#usage)
- [Detailed Descriptions](#detailed-descriptions)
  - [`rospinn.py`](#rospinnpy)
  - [`uart_comm.v`](#uart_commv)
  - [`top_L.v`](#top_lv)
  - [`cpu.v`](#cpuv)
  - [`fpga.v`](#fpgav)
  - [`main.py`](#mainpy)
  - [`mortymb.py`](#mortymbpy)
- [Appendix](#appendix)
  - [Power and Ground Connections](#power-and-ground-connections)
  - [Helper Function](#helper-function)
  - [Components](#components)
  - [Connections](#connections)
  - [Decoupling Capacitors](#decoupling-capacitors)
  - [GPIO Integration Plans](#gpio-integration-plans)
- [Conclusion](#conclusion)

## Overview

This project implements a bipedal humanoid control system using a Physics-Informed Neural Network (PINN) and Reinforcement Learning (RL) for stability and manipulation tasks. The system integrates with ROS for real-time control and utilizes FPGA for hardware acceleration.

## Directory Structure

- **`rospinn.py`**: Main ROS node script implementing the PINN and RL algorithms.
- **`uart_comm.v`**: Verilog module for UART communication with FPGA.
- **`top_L.v`**: Top-level Verilog module integrating all components.
- **`cpu.v`**: Verilog module for the CPU.
- **`fpga.v`**: Verilog module for the FPGA.
- **`main.py`**: Script to compile the Verilog modules and run the ROS node.
- **`mortymb.py`**: Defines the electronic components and connections for the robot’s motherboard using `gEDA`.
- **`README.md`**: This file.

## Dependencies

- ROS (Robot Operating System)
- Python 3.x
- PyTorch
- scikit-learn
- iverilog (for Verilog compilation)
- sKiDL (for electronic design)

## Setup

### Install Dependencies

Ensure all dependencies are installed using the following commands:
```sh
sudo apt-get install ros-humble-desktop-full
sudo apt-get install iverilog
pip install torch scikit-learn skidl
```

### Compile the Verilog Modules

Compile the Verilog modules using `iverilog` and `vvp`:
```sh
iverilog -o uart_comm uart_comm.v
iverilog -o top_L top_L.v
iverilog -o cpu cpu.v
iverilog -o fpga fpga.v
vvp uart_comm
vvp top_L
vvp cpu
vvp fpga
```

### Run the ROS Node

Start the ROS node that runs the PINN and RL algorithms:
```sh
rosrun rospinn rospinn.py
```

### Automate the Process

Alternatively, use the `main.py` script to compile the Verilog modules and run the ROS node:
```sh
python main.py
```

## Usage

The system is designed to control a bipedal humanoid robot. It subscribes to ROS topics for sensor data, including joint states and forces, and publishes control signals to actuate the robot's movements. The PINN model ensures stability and manipulation capabilities, while the RL agent optimizes control strategies over time.

## Detailed Descriptions

### `rospinn.py`

- **Purpose**: Implements the main control algorithms for the robot using PINN and RL within a ROS node.
- **Functionality**:
  - Initializes the ROS node.
  - Subscribes to sensor data topics (e.g., joint states, forces).
  - Publishes control signals to actuate the robot.
  - Utilizes a PINN to maintain stability and perform manipulation tasks.
  - Uses RL to optimize control strategies based on feedback.
___
## fpga subdirectory
### `uart_comm.v` 

- **Purpose**: Defines the Verilog module for UART communication with the FPGA.
- **Functionality**:
  - Implements UART communication protocols.
  - Facilitates data exchange between the FPGA and other components.

### `top_L.v`

- **Purpose**: Defines the top-level Verilog module integrating the CPU, FPGA, and UART modules.
- **Functionality**:
  - Connects the CPU, FPGA, and UART communication.
  - Manages data flow between components.

### `cpu.v`

- **Purpose**: Defines the Verilog module for the CPU.
- **Functionality**:
  - Implements the CPU operations and interfaces with the UART and FPGA modules.

### `fpga.v`

- **Purpose**: Defines the Verilog module for the FPGA.
- **Functionality**:
  - Implements FPGA operations and interfaces with the CPU and UART modules.

### `main.py`

- **Purpose**: Automates the compilation of the Verilog modules and execution of the ROS node.
- **Functionality**:
  - Compiles the Verilog modules using `iverilog` and `vvp`.
  - Runs the `rospinn.py` script using `rosrun`.
___

## Schematics and Assembly

### `mortymb.py`

- **Purpose**: Defines and connects the electronic components of the robot’s motherboard using `skidl` for electronic design automation.
- **Functionality**:
  - Defines power supply nets and various components (ESP32, CPU, RAM, FPGA, USB, Ethernet, UART, PMIC, Clock, TPU, and Flash memory).
  - Establishes connections between components.
  - Adds decoupling capacitors for power stability.
  - Generates netlist, schematic, and PCB layout files.
  - Includes error checking and reporting using ERC (Electrical Rule Check).

The `mortymb.py` script automates the process of creating a schematic for the motherboard by defining components, connecting them, and ensuring the design follows electrical rules. The script outputs the necessary files for further processing and PCB design.

## Appendix

*will be revised*

### Power and Ground Connections

- **GND**: Ground.
- **ESP32_VCC**: Power supply for the ESP32 module.
- **CPU_VCC**: Power supply for the CPU.
- **RAM_VCC**: Power supply for the RAM.
- **FPGA_VCC**: Power supply for the FPGA.
- **FPGA_GND**: Ground for FPGA.
- **USB_VCC**: Power supply for USB ports.
- **ETH_VCC**: Power supply for Ethernet controller and port.
- **UART_VCC**: Power supply for UART communication module.
- **PMIC_VCC**: Power supply from the Power Management IC.
- **TPU_VCC**: Power supply for TPU.
- **FLASH_VCC**: Power supply for Flash memory.

### Helper Function

- **add_decoupling_caps(part, pin_name, gnd, num_caps=2)**:
  - Adds decoupling capacitors to a specified part and pin.
  - Decoupling capacitors help stabilize the power supply to the components.

### Components

The script defines the following components:

- **ESP32**: ESP32-WROOM-32 module.
- **CPU**: ATmega2560.
- **RAM**: MT48LC16M16A2P-75 (SDRAM).
- **FPGA**: Xilinx XC7A35T-1FTG256C.
- **UART Communication**: MAX232.
- **PMIC**: TPS65217.
- **USB Controller**: USB3320C-EZK.
- **USB Ports**: Multiple USB ports.
- **Ethernet Controller**: LAN8720.
- **Ethernet Port**: RJ45 Ethernet port.
- **Clock Generator**: SI5351A-B-GT.
- **TPU**: Edge TPU.
- **Flash Memory**: W25Q64FVSSIG.

### Connections

The `mortymb.py` script establishes connections for power and data lines between components:

- **Power and Ground Connections**:
  - Connects each component’s power and ground pins to the respective power nets.
  - Example: `vcc += cpu['VCC']`.

- **CPU and RAM**:
  - Connects address and data lines between the CPU and RAM modules.
  - Example: `cpu['AD0', 'AD1', ...] += ram['DQ0', 'DQ1', ...]`.

- **FPGA**:
  - Connects FPGA power and ground pins.
  - Example: `vcc += fpga['VCC']`.

- **UART Communication**:
  - Connects UART communication lines between the ESP32, CPU, and UART module.
  - Example: `esp32['GPIO1'] += uart['T1IN']`.

- **ESP32 to USB**:
  - Connects data lines between ESP32 and USB controller.
  - Example: `esp32['GPIO21'] += usb['DP']`.

- **ESP32 to Ethernet**:
  - Connects data lines between ESP32 and Ethernet controller.
  - Example: `esp32['GPIO0'] += eth['TXEN']`.

- **PMIC**:
  - Connects the PMIC to provide regulated power to various components.
  - Example: `pmic['OUT1'] += cpu['VCC']`.

### GPIO Capabilities

The current design includes GPIO (General Purpose Input/Output) integration for enhanced sensor interfacing and integral control capabilities, making the system versatile for future expansions and customizations.

## Conclusion

This project aims to provide a comprehensive system for controlling a bipedal humanoid robot. By integrating advanced hardware with sophisticated software algorithms, the robot can achieve stable and optimized performance in real-time environments.
