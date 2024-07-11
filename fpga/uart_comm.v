module uart_comm (
    input wire clk,
    input wire reset,
    input wire [31:0] data_in,
    output reg [31:0] data_out,
    input wire uart_rx,
    output reg uart_tx
);

reg [7:0] rx_buffer;
reg [7:0] tx_buffer;
reg [3:0] bit_counter_rx;
reg [3:0] bit_counter_tx;
reg [9:0] baud_rate_counter;
reg [1:0] state_rx;
reg [1:0] state_tx;
reg rx_ready;
reg tx_ready;

// Baud rate generator parameters
parameter integer BAUD_RATE_DIV = 10416; // Example parameter, should be adjusted based on clock frequency and desired baud rate

always @(posedge clk or posedge reset) begin
    if (reset) begin
        data_out <= 32'b0;
        rx_buffer <= 8'b0;
        tx_buffer <= 8'b0;
        bit_counter_rx <= 4'b0;
        bit_counter_tx <= 4'b0;
        baud_rate_counter <= 0;
        state_rx <= 0;
        state_tx <= 0;
        rx_ready <= 0;
        tx_ready <= 0;
        uart_tx <= 1'b1; // Idle state for UART TX
    end else begin
        // Baud rate generation
        if (baud_rate_counter < BAUD_RATE_DIV) begin
            baud_rate_counter <= baud_rate_counter + 1;
        end else begin
            baud_rate_counter <= 0;
            
            // UART Receive State Machine
            case (state_rx)
                0: begin
                    if (uart_rx == 0) begin // Start bit detected
                        state_rx <= 1;
                        bit_counter_rx <= 0;
                    end
                end
                1: begin
                    rx_buffer[bit_counter_rx] <= uart_rx;
                    bit_counter_rx <= bit_counter_rx + 1;
                    if (bit_counter_rx == 7) begin
                        state_rx <= 2;
                    end
                end
                2: begin
                    data_out <= {data_out[23:0], rx_buffer}; // Move data to data_out
                    state_rx <= 0;
                end
            endcase
            
            // UART Transmit State Machine
            case (state_tx)
                0: begin
                    if (data_in[31:24] != 8'b0) begin // Data ready to transmit
                        tx_buffer <= data_in[31:24];
                        state_tx <= 1;
                        bit_counter_tx <= 0;
                        uart_tx <= 0; // Start bit
                    end
                end
                1: begin
                    uart_tx <= tx_buffer[bit_counter_tx];
                    bit_counter_tx <= bit_counter_tx + 1;
                    if (bit_counter_tx == 7) begin
                        state_tx <= 2;
                    end
                end
                2: begin
                    uart_tx <= 1; // Stop bit
                    state_tx <= 0;
                end
            endcase
        end
    end
end

endmodule