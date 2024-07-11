module uart_comm(
    input wire clk,
    input wire reset,
    input wire [31:0] data_in,
    output reg [31:0] data_out,
    input wire uart_rx,
    output wire uart_tx
);

reg [7:0] rx_buffer;
reg [7:0] tx_buffer;
reg [3:0] bit_counter_rx;
reg [3:0] bit_counter_tx;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        data_out <= 32'b0;
        rx_buffer <= 8'b0;
        tx_buffer <= 8'b0;
        bit_counter_rx <= 4'b0;
        bit_counter_tx <= 4'b0;
    end else begin
        // UART Receive
        if (uart_rx) begin
            if (bit_counter_rx < 8) begin
                rx_buffer[bit_counter_rx] <= uart_rx;
                bit_counter_rx <= bit_counter_rx + 1;
            end else begin
                data_out <= {data_out[23:0], rx_buffer};
                bit_counter_rx <= 0;
            end
        end
        
        // UART Transmit
        if (data_in[31:24] != 8'b0) begin
            if (bit_counter_tx < 8) begin
                tx_buffer[bit_counter_tx] <= data_in[31-bit_counter_tx];
                bit_counter_tx <= bit_counter_tx + 1;
            end else begin
                bit_counter_tx <= 0;
            end
        end
    end
end

assign uart_tx = tx_buffer[0];

endmodule