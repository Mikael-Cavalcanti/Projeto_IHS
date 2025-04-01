module bancoReg(
            input write, 
            input clk,
            input nrst,
            input logic [5-1:0] regreader1,
            input logic [5-1:0] regreader2,
            input logic [5-1:0] regwriteaddress,
            input logic [64-1:0] datain,
            output logic [64-1:0] dataout1,
            output logic [64-1:0] dataout2
        );

//timeunit        1ns ;
//timeprecision 100ps ;

logic [64-1:0] regs [0:31]; 
assign dataout1 = regs[regreader1];
assign dataout2 = regs[regreader2];

always_ff@(posedge clk or negedge nrst)
begin
	if(~nrst)
  	begin
  		regs <= '{default:32'd0};
	end
  	else begin
		if(write)
		begin  	   
		    regs[regwriteaddress] <= datain;
		end
	end
end

endmodule
