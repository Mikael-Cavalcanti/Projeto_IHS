module register(
            input clk,
            input nrst,
            input regWrite,
            input logic [64-1:0] DadoIn,
            output logic [64-1:0] DadoOut
        );

always_ff @(posedge clk or negedge nrst)
begin	
	if(~nrst)
		DadoOut <= 64'd0;
	else
	begin
		if (regWrite) begin
		    DadoOut <= DadoIn;
		end
	end		
end
endmodule 
