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
- **`mortymb.py`**: Defines the electronic components and connections for the robot’s motherboard using `skidl`.
- **`README.md`**: This file.

## Dependencies

- ROS (Robot Operating System)
- Python 3.x
- PyTorch
- scikit-learn
- iverilog (for Verilog compilation)
- skidl (for electronic design)

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
## Schematics and assembly
### `mortymb.py`

- **Purpose**: Defines and connects the electronic components of the robot’s motherboard using `skidl`.
- **Functionality**:
  - Defines power supply nets and various components (CPU, RAM, FPGA, PCIe slots, GPUs, USB, Ethernet, and SATA controllers).
  - Establishes connections between components.
  - Adds decoupling capacitors for power stability.
  - Generates netlist, schematic, and PCB layout files.

## Appendix

### Power and Ground Connections

- **GND**: Ground.
- **PCIE_VCC**: Power supply for PCIe slots and GPUs.
- **PCIE_GND**: Ground for PCIe slots and GPUs.
- **USB_VCC**: Power supply for USB ports.
- **ETH_VCC**: Power supply for Ethernet controller and port.
- **SATA_VCC**: Power supply for SATA controller and ports.
- **FPGA_VCC**: Power supply for FPGA.
- **FPGA_GND**: Ground for FPGA.

### Helper Function

- **add_decoupling_caps(part, pin_name, gnd, num_caps=2)**:
  - Adds decoupling capacitors to a specified part and pin.
  - Decoupling capacitors help stabilize the power supply to the components.

### Components

The script defines the following components:

- **CPU**: AMD Ryzen9 7950X.
- **RAM**: Two DDR4 memory modules.
- **FPGA**: Xilinx Spartan6.
- **UART Communication**: Custom UART communication module.
- **PCIe Slots**: Six PCIe slots.
- **GPUs**: Six AMD Radeon RX GPUs.
- **PMIC**: Power Management IC (TI TPS65217).
- **ATX Power**: ATX power connector.
- **USB Controller**: NEC D720200.
- **USB Ports**: Four USB ports.
- **Ethernet Controller**: Realtek RTL8111.
- **Ethernet Port**: RJ45 Ethernet port.
- **SATA Controller**: Marvell 88SE9215.
- **SATA Ports**: Four SATA ports.
- **Clock Generator**: IDT 5V9885.
- **VRMs**: Voltage Regulator Modules for different power nets.

### Connections

The `mortymb.py` script establishes connections for power and data lines between components:

- **Power and Ground Connections**:
  - Connects each component’s power and ground pins to the respective power nets.
  - Example: `power_nets['VCC'] += cpu['VCC']`.

- **CPU and RAM**:
  - Connects address and data lines between the CPU and RAM modules.
  - Example: `cpu['ADDR0', 'ADDR1', ...] += ram[0]['ADDR0', 'ADDR1', ...]`.

- **FPGA**:
  - Connects FPGA power and ground pins.
  - Example: `power_nets['FPGA_VCC'] += fpga['VCC']`.

- **UART Communication**:
  - Connects UART communication lines between the CPU, UART module, and FPGA.
  - Example: `cpu['UART_TX'] += uart_comm['uart_rx']`.

- **PCIe Slots and GPUs**:
  - Connects power, ground, and data lines between PCIe slots, GPUs, and CPU.
  - Example: `power_nets['PCIE_VCC'] += pcie_slots[0]['VCC'], gpus[0]['PCIE_VCC']`.

- **PMIC**:
  - Connects the PMIC to provide regulated power to the CPU and RAM.
  - Example: `pmic['OUT1'] += cpu['VCC']`.

### GPIO Integration Plans

For future expansion, the project plans to integrate GPIO (General Purpose Input/Output) for enhanced sensor interfacing and integral control capabilities.

## Conclusion

This project provides a comprehensive system for controlling a bipedal humanoid robot. By integrating advanced hardware with sophisticated software algorithms, the robot can achieve stable and optimized performance in real-time environments.
