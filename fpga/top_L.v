module top_level (
    input wire clk,
    input wire reset,
    input wire uart_rx,
    output wire uart_tx,
    output wire [31:0] debug_data_out
);

// Internal signals
wire [31:0] cpu_data_out;
wire [31:0] fpga_data_in;
wire [31:0] fpga_processed_data;
wire [1:0] cpu_error_flag;
wire [1:0] fpga_error_flag;
wire [1:0] uart_error_flags;

// Instantiate the CPU
cpu_module cpu_instance (
    .clk(clk),
    .reset(reset),
    .data_out(cpu_data_out),
    .error_flag(cpu_error_flag)
);

// Instantiate the FPGA
fpga_module fpga_instance (
    .clk(clk),
    .reset(reset),
    .data_in(fpga_data_in),
    .processed_data(fpga_processed_data),
    .error_flag(fpga_error_flag)
);

// Instantiate the UART module
uart_comm uart_instance (
    .clk(clk),
    .reset(reset),
    .data_in(cpu_data_out),
    .data_out(fpga_data_in),
    .uart_rx(uart_rx),
    .uart_tx(uart_tx),
    .error_flags(uart_error_flags)
);

// Combine error flags for monitoring and add processed FPGA data to debug output
assign debug_data_out = {cpu_error_flag, fpga_error_flag, uart_error_flags, fpga_processed_data[25:0]};

endmodule