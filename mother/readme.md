# Complete Advanced Motherboard Design
*(all is kind of a placeholder as this is not the board; though, it will be the basis of another project.)*
___
## Overview
This project involves the design of an advanced motherboard using the Skidl library for schematic generation. The design integrates various high-performance components, including an AMD Ryzen 9 7950X CPU, DDR4 RAM modules, a Xilinx Spartan-6 FPGA, PCIe slots for GPUs, and multiple controllers for USB, Ethernet, and SATA. The design ensures efficient power distribution and signal routing, providing a robust platform for high-performance computing applications.
___
![mortDiagram](https://github.com/HermiTech-LLC/Morty/blob/main/Images/MortDiagram.PNG)
___
## Power Distribution

### Main Power Input
- **Primary Voltage:** 12V
- **Source:** ATX Power Supply

### Power Regulation
The main 12V input is regulated down to the required voltages for various components using Voltage Regulator Modules (VRMs) and a Power Management IC (PMIC).

### Components and Power Requirements

1. **CPU (AMD Ryzen 9 7950X)**
   - **Voltage:** 1.35V
   - **Current:** 105A
   - **Power Consumption:** 141.75W
   - **Regulation:** VRM

2. **DDR4 RAM Modules (2x)**
   - **Voltage:** 1.2V
   - **Current:** 1A per module
   - **Power Consumption:** 1.2W per module, 2.4W total
   - **Regulation:** VRM

3. **Xilinx Spartan-6 FPGA**
   - **Core Voltage:** 1.2V
   - **Core Current:** 1A
   - **I/O Voltage:** 3.3V
   - **I/O Current:** 0.5A
   - **Power Consumption:** 1.2W (core) + 1.65W (I/O) = 2.85W
   - **Regulation:** VRM

4. **PCIe Slots for GPUs (6x)**
   - **Main Voltage:** 12V
   - **Current per slot:** 6A
   - **Auxiliary Voltage:** 3.3V
   - **Power Consumption per slot:** 72W
   - **Total Power Consumption:** 432W
   - **Regulation:** Direct 12V input

5. **Power Management IC (TI TPS65217)**
   - **Input Voltage:** 12V
   - **Output Voltages:** 1.2V, 3.3V, 5V
   - **Power Consumption:** Approx. 10W
   - **Regulation:** Internal

6. **USB Controller (NEC D720200)**
   - **Voltage:** 3.3V
   - **Current:** 0.5A
   - **Power Consumption:** 1.65W
   - **Regulation:** VRM

7. **USB Ports (4x)**
   - **Voltage:** 5V
   - **Current per port:** 0.9A
   - **Power Consumption per port:** 4.5W
   - **Total Power Consumption:** 18W
   - **Regulation:** VRM

8. **Ethernet Controller (Realtek RTL8111)**
   - **Voltage:** 3.3V
   - **Current:** 0.25A
   - **Power Consumption:** 0.825W
   - **Regulation:** VRM

9. **Ethernet Port**
   - **Voltage:** 3.3V
   - **Current:** 0.25A
   - **Power Consumption:** 0.825W
   - **Regulation:** VRM

10. **SATA Controller (Marvell 88SE9215)**
    - **Voltage:** 3.3V
    - **Current:** 0.3A
    - **Power Consumption:** 0.99W
    - **Regulation:** VRM

11. **SATA Ports (4x)**
    - **Voltage:** 5V
    - **Current per port:** 0.5A
    - **Power Consumption per port:** 2.5W
    - **Total Power Consumption:** 10W
    - **Regulation:** VRM

12. **Clock Generator (IDT 5V9885)**
    - **Voltage:** 3.3V
    - **Current:** 0.1A
    - **Power Consumption:** 0.33W
    - **Regulation:** VRM

### Total Power Consumption
- **CPU:** 141.75W
- **RAM Modules:** 2.4W
- **FPGA:** 2.85W
- **PCIe Slots (6x GPUs):** 432W
- **Power Management IC:** 10W
- **USB Controller and Ports:** 19.65W
- **Ethernet Controller and Port:** 1.65W
- **SATA Controller and Ports:** 10.99W
- **Clock Generator:** 0.33W
- **Total Power Consumption:** Approximately 622.62W

### Conclusion
This motherboard design efficiently distributes power across various high-performance components, ensuring stable operation and high efficiency. The primary 12V input is effectively regulated to meet the specific voltage and current requirements of each component, providing a reliable platform for high-performance applications.
