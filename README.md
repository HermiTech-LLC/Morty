# Bipedal Humanoid Control System
___
![img](https://github.com/HermiTech-LLC/Morty/blob/main/Images/Mort.jpg)
___
## Overview

This project implements a bipedal humanoid control system using a Physics-Informed Neural Network (PINN) and Reinforcement Learning (RL) for stability and manipulation tasks. The system integrates with ROS for real-time control and utilizes FPGA for hardware acceleration.

## Directory Structure

- `rospinn.py`: The main ROS node script implementing the PINN and RL algorithms.
- `uart_comm.v`: Verilog module for UART communication with FPGA.
- `main.py`: Script to compile the Verilog module and run the ROS node.
- `mortymb.py`: Defines the electronic components and connections for the robot’s motherboard using `skidl`.
- `README.md`: This file.

## Dependencies

- ROS (Robot Operating System)
- Python 3.x
- PyTorch
- scikit-learn
- iverilog (for Verilog compilation)
- skidl (for electronic design)

## Setup

1. **Install Dependencies**:
   Ensure all dependencies are installed. You can install them using the following commands:
   ```sh
   sudo apt-get install ros-humble-desktop-full
   sudo apt-get install iverilog
   pip install torch scikit-learn skidl
   ```

2. **Compile the Verilog Module**:
   Compile the Verilog module for UART communication with the FPGA using `iverilog` and `vvp`:
   ```sh
   iverilog -o uart_comm uart_comm.v
   vvp uart_comm
   ```

3. **Run the ROS Node**:
   Start the ROS node that runs the PINN and RL algorithms:
   ```sh
   rosrun rospinn rospinn.py
   ```

4. **Automate the Process**:
   Alternatively, you can use the `main.py` script to compile the Verilog module and run the ROS node:
   ```sh
   python main.py
   ```

## Usage

The system is designed to control a bipedal humanoid robot. It subscribes to ROS topics for sensor data, including joint states and forces, and publishes control signals to actuate the robot's movements. The PINN model ensures stability and manipulation capabilities, while the RL agent optimizes control strategies over time.

## Detailed Descriptions

### rospinn.py

- **Purpose**: Implements the main control algorithms for the robot using PINN and RL within a ROS node.
- **Functionality**:
  - Initializes the ROS node.
  - Subscribes to sensor data topics (e.g., joint states, forces).
  - Publishes control signals to actuate the robot.
  - Utilizes a PINN to maintain stability and perform manipulation tasks.
  - Uses RL to optimize control strategies based on feedback.

### uart_comm.v

- **Purpose**: Defines the Verilog module for UART communication with the FPGA.
- **Functionality**:
  - Implements UART communication protocols.
  - Facilitates data exchange between the FPGA and other components.

### main.py

- **Purpose**: Automates the compilation of the Verilog module and execution of the ROS node.
- **Functionality**:
  - Compiles the Verilog module using `iverilog` and `vvp`.
  - Runs the `rospinn.py` script using `rosrun`.

### mortymb.py

- **Purpose**: Defines and connects the electronic components of the robot’s motherboard using `skidl`.
- **Functionality**:
  - Defines power supply nets and various components (CPU, RAM, FPGA, PCIe slots, GPUs, USB, Ethernet, and SATA controllers).
  - Establishes connections between components.
  - Adds decoupling capacitors for power stability.
  - Generates netlist, schematic, and PCB layout files.

## Conclusion

This project provides a comprehensive system for controlling a bipedal humanoid robot. By integrating advanced hardware with sophisticated software algorithms, the robot can achieve stable and optimized performance in real-time environments.
