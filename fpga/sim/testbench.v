module testbench;

reg clk;
reg reset;
reg uart_rx;
wire uart_tx;

top_level uut (
    .clk(clk),
    .reset(reset),
    .uart_rx(uart_rx),
    .uart_tx(uart_tx)
);

initial begin
    clk = 0;
    forever #5 clk = ~clk; // 100 MHz clock
end

initial begin
    // Initial reset
    reset = 1;
    #20;
    reset = 0;

    // Simulate UART communication
    uart_rx = 1; // Idle state
    #100;
    uart_rx = 0; // Start bit
    #100;
    uart_rx = 1; // Data bit 0
    #100;
    uart_rx = 0; // Data bit 1
    #100;
    uart_rx = 1; // Data bit 2
    #100;
    uart_rx = 0; // Data bit 3
    #100;
    uart_rx = 1; // Data bit 4
    #100;
    uart_rx = 0; // Data bit 5
    #100;
    uart_rx = 1; // Data bit 6
    #100;
    uart_rx = 0; // Data bit 7
    #100;
    uart_rx = 1; // Stop bit
    #100;

    // Further simulation logic here

    #1000;
    $stop;
end

endmodule