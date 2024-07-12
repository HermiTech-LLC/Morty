module fpga_module (
    input wire clk,
    input wire reset,
    input wire [31:0] data_in,
    output reg [31:0] processed_data,
    output reg error_flag
);

// Internal signals
reg [31:0] internal_data;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        internal_data <= 32'b0;
        processed_data <= 32'b0;
        error_flag <= 1'b0;
    end else begin
        // Data processing logic
        internal_data <= data_in + 32'hA5A5A5A5;
        processed_data <= internal_data;

        // Error checking
        if (processed_data > 32'hFFFFFF00) begin
            error_flag <= 1'b1;
        end else begin
            error_flag <= 1'b0;
        end
    end
end

endmodule