module testbench;

reg clk;
reg reset;
reg uart_rx;
wire uart_tx;
wire [31:0] debug_data_out;

top_level uut (
    .clk(clk),
    .reset(reset),
    .uart_rx(uart_rx),
    .uart_tx(uart_tx),
    .debug_data_out(debug_data_out)
);

// Clock generation: 100 MHz clock (period = 10ns)
initial begin
    clk = 0;
    forever #5 clk = ~clk;
end

// Task for UART transmission
task send_uart_byte;
    input [7:0] byte;
    integer i;
    begin
        uart_rx = 0; // Start bit
        #104160; // BAUD_RATE_DIV for start bit (assuming 9600 baud rate)
        for (i = 0; i < 8; i = i + 1) begin
            uart_rx = byte[i]; // Data bits
            #104160; // BAUD_RATE_DIV for each data bit
        end
        uart_rx = 1; // Stop bit
        #104160; // BAUD_RATE_DIV for stop bit
    end
endtask

initial begin
    // Initial reset
    reset = 1;
    #20;
    reset = 0;

    // Initial idle state
    uart_rx = 1;

    // Simulate UART communication
    send_uart_byte(8'b10101010); // Sending 0xAA
    #200000; // Wait before next byte

    send_uart_byte(8'b11001100); // Sending 0xCC
    #200000; // Wait before next byte

    send_uart_byte(8'b11110000); // Sending 0xF0
    #200000; // Wait before next byte

    // Further simulation logic
    #1000;

    // Monitor debug_data_out
    $monitor("Time: %0t | debug_data_out: %h | CPU Error Flag: %b | FPGA Error Flag: %b | UART Error Flags: %b", 
             $time, debug_data_out, debug_data_out[31:30], debug_data_out[29:28], debug_data_out[27:26]);

    // Stop simulation after some time
    #500000;
    $stop;
end

endmodule