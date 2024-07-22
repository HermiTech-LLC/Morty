<?xml version='1.0' encoding='UTF-8'?>
<schematic>
  <components>
    <component name="cpu" x="10" y="20"/>
    <component name="ram1" x="30" y="20"/>
    <component name="ram2" x="50" y="20"/>
    <component name="fpga" x="70" y="20"/>
    <component name="uart_comm" x="90" y="20"/>
    <component name="pcie_slot1" x="110" y="20"/>
    <component name="pcie_slot2" x="130" y="20"/>
    <component name="gpu1" x="150" y="20"/>
    <component name="gpu2" x="170" y="20"/>
    <component name="pmic" x="190" y="20"/>
    <component name="atx_power" x="210" y="20"/>
    <component name="usb_ctrl" x="230" y="20"/>
    <component name="usb_port1" x="250" y="20"/>
    <component name="usb_port2" x="270" y="20"/>
    <component name="eth_ctrl" x="290" y="20"/>
    <component name="eth_port" x="310" y="20"/>
    <component name="sata_ctrl" x="330" y="20"/>
    <component name="sata_port1" x="350" y="20"/>
    <component name="clock_gen" x="370" y="20"/>
    <component name="C_cpu_VCC_0" x="0" y="0"/>
    <component name="C_cpu_VCC_1" x="0" y="0"/>
    <component name="C_ram1_VCC_0" x="0" y="0"/>
    <component name="C_ram1_VCC_1" x="0" y="0"/>
    <component name="C_ram2_VCC_0" x="0" y="0"/>
    <component name="C_ram2_VCC_1" x="0" y="0"/>
    <component name="C_usb_ctrl_VCC_0" x="0" y="0"/>
    <component name="C_usb_ctrl_VCC_1" x="0" y="0"/>
    <component name="C_eth_ctrl_VCC_0" x="0" y="0"/>
    <component name="C_eth_ctrl_VCC_1" x="0" y="0"/>
    <component name="C_sata_ctrl_VCC_0" x="0" y="0"/>
    <component name="C_sata_ctrl_VCC_1" x="0" y="0"/>
    <component name="C_clock_gen_VCC_0" x="0" y="0"/>
    <component name="C_clock_gen_VCC_1" x="0" y="0"/>
    <component name="C_fpga_VCC_0" x="0" y="0"/>
    <component name="C_fpga_VCC_1" x="0" y="0"/>
  </components>
  <nets>
    <net name="VCC">
      <connection component="cpu" pin="VCC"/>
      <connection component="ram1" pin="VCC"/>
      <connection component="ram2" pin="VCC"/>
      <connection component="fpga" pin="VCC"/>
      <connection component="pmic" pin="VCC"/>
      <connection component="usb_ctrl" pin="VCC"/>
      <connection component="eth_ctrl" pin="VCC"/>
      <connection component="sata_ctrl" pin="VCC"/>
      <connection component="clock_gen" pin="VCC"/>
    </net>
    <net name="GND">
      <connection component="cpu" pin="GND"/>
      <connection component="ram1" pin="GND"/>
      <connection component="ram2" pin="GND"/>
      <connection component="fpga" pin="GND"/>
      <connection component="pmic" pin="GND"/>
      <connection component="usb_ctrl" pin="GND"/>
      <connection component="eth_ctrl" pin="GND"/>
      <connection component="sata_ctrl" pin="GND"/>
      <connection component="clock_gen" pin="GND"/>
    </net>
    <net name="C_cpu_VCC_0">
      <connection component="C_cpu_VCC_0" pin="1"/>
      <connection component="cpu" pin="VCC"/>
      <connection component="C_cpu_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_cpu_VCC_1">
      <connection component="C_cpu_VCC_1" pin="1"/>
      <connection component="cpu" pin="VCC"/>
      <connection component="C_cpu_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_ram1_VCC_0">
      <connection component="C_ram1_VCC_0" pin="1"/>
      <connection component="ram1" pin="VCC"/>
      <connection component="C_ram1_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_ram1_VCC_1">
      <connection component="C_ram1_VCC_1" pin="1"/>
      <connection component="ram1" pin="VCC"/>
      <connection component="C_ram1_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_ram2_VCC_0">
      <connection component="C_ram2_VCC_0" pin="1"/>
      <connection component="ram2" pin="VCC"/>
      <connection component="C_ram2_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_ram2_VCC_1">
      <connection component="C_ram2_VCC_1" pin="1"/>
      <connection component="ram2" pin="VCC"/>
      <connection component="C_ram2_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_usb_ctrl_VCC_0">
      <connection component="C_usb_ctrl_VCC_0" pin="1"/>
      <connection component="usb_ctrl" pin="VCC"/>
      <connection component="C_usb_ctrl_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_usb_ctrl_VCC_1">
      <connection component="C_usb_ctrl_VCC_1" pin="1"/>
      <connection component="usb_ctrl" pin="VCC"/>
      <connection component="C_usb_ctrl_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_eth_ctrl_VCC_0">
      <connection component="C_eth_ctrl_VCC_0" pin="1"/>
      <connection component="eth_ctrl" pin="VCC"/>
      <connection component="C_eth_ctrl_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_eth_ctrl_VCC_1">
      <connection component="C_eth_ctrl_VCC_1" pin="1"/>
      <connection component="eth_ctrl" pin="VCC"/>
      <connection component="C_eth_ctrl_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_sata_ctrl_VCC_0">
      <connection component="C_sata_ctrl_VCC_0" pin="1"/>
      <connection component="sata_ctrl" pin="VCC"/>
      <connection component="C_sata_ctrl_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_sata_ctrl_VCC_1">
      <connection component="C_sata_ctrl_VCC_1" pin="1"/>
      <connection component="sata_ctrl" pin="VCC"/>
      <connection component="C_sata_ctrl_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_clock_gen_VCC_0">
      <connection component="C_clock_gen_VCC_0" pin="1"/>
      <connection component="clock_gen" pin="VCC"/>
      <connection component="C_clock_gen_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_clock_gen_VCC_1">
      <connection component="C_clock_gen_VCC_1" pin="1"/>
      <connection component="clock_gen" pin="VCC"/>
      <connection component="C_clock_gen_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_fpga_VCC_0">
      <connection component="C_fpga_VCC_0" pin="1"/>
      <connection component="fpga" pin="VCC"/>
      <connection component="C_fpga_VCC_0" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
    <net name="C_fpga_VCC_1">
      <connection component="C_fpga_VCC_1" pin="1"/>
      <connection component="fpga" pin="VCC"/>
      <connection component="C_fpga_VCC_1" pin="2"/>
      <connection component="GND" pin=""/>
    </net>
  </nets>
</schematic>
