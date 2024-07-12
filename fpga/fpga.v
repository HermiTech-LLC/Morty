module fpga_module (
    input wire clk,
    input wire reset,
    input wire [31:0] data_in,
    output reg [31:0] processed_data,
    output reg [1:0] error_flag
);

// Internal signals
reg [31:0] internal_data;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        internal_data <= 32'b0;
        processed_data <= 32'b0;
        error_flag <= 2'b0;
    end else begin
        // Data processing logic
        internal_data <= data_in + 32'hA5A5A5A5;
        processed_data <= internal_data;

        // Error checking
        if (processed_data > 32'hFFFFFF00) begin
            error_flag[0] <= 1'b1; // Overflow error flag
        end else begin
            error_flag[0] <= 1'b0;
        end

        // Additional error check (e.g., even number check)
        if (processed_data[0] == 1'b0) begin
            error_flag[1] <= 1'b1; // Even number error flag
        end else begin
            error_flag[1] <= 1'b0;
        end
    end
end

endmodule