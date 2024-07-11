module fpga_module (
    input wire clk,
    input wire reset,
    input wire [31:0] data_in
);

reg [31:0] received_data;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        received_data <= 32'b0;
    end else begin
        received_data <= data_in;
        // Example data handling logic
    end
end

endmodule