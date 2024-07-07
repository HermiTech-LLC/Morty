# Bipedal Humanoid Control System

## Overview

This project implements a bipedal humanoid control system using a Physics-Informed Neural Network (PINN) and Reinforcement Learning (RL) for stability and manipulation tasks. The system integrates with ROS for real-time control and utilizes FPGA for hardware acceleration.

## Directory Structure

- `rospinn_part1.py`: The first part of the main ROS node script implementing the PINN and RL algorithms.
- `rospinn_part2.py`: The second part of the main ROS node script implementing the PINN and RL algorithms.
- `rospinn_part3.py`: The third part of the main ROS node script implementing the PINN and RL algorithms.
- `rospinn_part4.py`: The fourth part of the main ROS node script implementing the PINN and RL algorithms.
- `uart_comm.v`: Verilog module for UART communication with FPGA.
- `main.py`: Script to compile the Verilog module and run the ROS node.
- `README.md`: This file.

## Dependencies

- ROS (Robot Operating System)
- Python 3.x
- PyTorch
- scikit-learn
- iverilog (for Verilog compilation)

## Setup

1. Ensure all dependencies are installed.
2. Compile the Verilog module:
   ```sh
   iverilog -o uart_comm uart_comm.v
   vvp uart_comm
   ```

3. Run the ROS node:
   ```sh
   rosrun rospinn rospinn.py
   ```

4. Alternatively, you can use the `main.py` script to automate the process:
   ```sh
   python main.py
   ```

## Usage

The system subscribes to ROS topics for sensor data (joint states, forces) and publishes control signals. The PINN model ensures stability and manipulation capabilities, while the RL agent optimizes control strategies.
