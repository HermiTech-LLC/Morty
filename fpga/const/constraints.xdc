# Clock signal constraints
set_property PACKAGE_PIN PIOA [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]
# Specify the clock frequency (optional, if known)
create_clock -period 10.000 [get_ports clk]

# Reset signal constraints
set_property PACKAGE_PIN PIOB [get_ports reset]
set_property IOSTANDARD LVCMOS33 [get_ports reset]

# UART receive signal constraints
set_property PACKAGE_PIN PIOC [get_ports uart_rx]
set_property IOSTANDARD LVCMOS33 [get_ports uart_rx]

# UART transmit signal constraints
set_property PACKAGE_PIN PIOD [get_ports uart_tx]
set_property IOSTANDARD LVCMOS33 [get_ports uart_tx]

# Optional: Add more signal constraints if needed
# Example for additional signals
# set_property PACKAGE_PIN PIOE [get_ports some_other_signal]
# set_property IOSTANDARD LVCMOS33 [get_ports some_other_signal]