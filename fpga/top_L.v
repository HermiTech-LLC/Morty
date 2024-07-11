module top_level (
    input wire clk,
    input wire reset,
    input wire uart_rx,
    output wire uart_tx
);

wire [31:0] cpu_data_out;
wire [31:0] fpga_data_in;

// Instantiate the CPU
cpu_module cpu_instance (
    .clk(clk),
    .reset(reset),
    .data_out(cpu_data_out)
);

// Instantiate the FPGA
fpga_module fpga_instance (
    .clk(clk),
    .reset(reset),
    .data_in(fpga_data_in)
);

// Instantiate the UART module
uart_comm uart_instance (
    .clk(clk),
    .reset(reset),
    .data_in(cpu_data_out),  // Connect CPU data output to UART data input
    .data_out(fpga_data_in), // Connect UART data output to FPGA data input
    .uart_rx(uart_rx),
    .uart_tx(uart_tx)
);

endmodule