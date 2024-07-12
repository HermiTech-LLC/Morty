# FPGA Component Modules

This repository contains the Verilog files and related resources for the FPGA project. The project includes several key modules such as the CPU, FPGA core, UART communication, and top-level integration.
___
![FPGAdiagram](https://github.com/HermiTech-LLC/Morty/blob/main/Images/FPGAdiagram.PNG)
___

## Directory Structure
___
```
fpga/
│
├── const/                 # Constraint files
├── sim/                   # Simulation files
├── cpu.v                  # CPU module Verilog file
├── fpga.v                 # FPGA core module Verilog file
├── top_L.v                # Top-level integration Verilog file
└── uart_comm.v            # UART communication module Verilog file
```
___

## Files and Modules

### `cpu.v`

This file defines the `cpu_module`, which is responsible for the core processing tasks within the FPGA. The module includes the following main components:

- **Inputs:**
  - `clk`: Clock signal
  - `reset`: Reset signal

- **Outputs:**
  - `data_out`: Data output signal
  - `error_flag`: Error flag signal

### `fpga.v`

This file defines the `fpga_module`, which represents the main FPGA core. The module includes the following main components:

- **Inputs:**
  - `clk`: Clock signal
  - `reset`: Reset signal
  - `data_in`: Data input signal

- **Outputs:**
  - `processed_data`: Processed data output signal
  - `error_flag`: Error flag signal

### `top_L.v`

This file defines the top-level module `top_level` that integrates the CPU, FPGA core, and UART communication modules. The module includes the following main components:

- **Inputs:**
  - `clk`: Clock signal
  - `reset`: Reset signal
  - `uart_rx`: UART receive signal

- **Outputs:**
  - `uart_tx`: UART transmit signal
  - `debug_data_out`: Debug data output signal

- **Internal Signals:**
  - `cpu_data_out`: Data output from CPU
  - `fpga_data_in`: Data input to FPGA
  - `cpu_error_flag`: Error flag from CPU
  - `fpga_error_flag`: Error flag from FPGA

### `uart_comm.v`

This file defines the `uart_comm` module, which handles UART communication between the FPGA and external devices. The module includes the following main components:

- **Inputs:**
  - `clk`: Clock signal
  - `reset`: Reset signal
  - `data_in`: Data input signal
  - `uart_rx`: UART receive signal

- **Outputs:**
  - `data_out`: Data output signal
  - `uart_tx`: UART transmit signal
  - `error_flags`: Error flag signals
