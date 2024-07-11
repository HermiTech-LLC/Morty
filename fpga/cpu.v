module cpu_module (
    input wire clk,
    input wire reset,
    output reg [31:0] data_out
);

always @(posedge clk or posedge reset) begin
    if (reset) begin
        data_out <= 32'b0;
    end else begin
        // Example data output logic
        data_out <= 32'hA5A5A5A5; // Example data
    end
end

endmodule