//This file contains (various) parameterized Carry Save Multiplier module(s)

module csmulti_fullbasecell#(parameter bitsize = 8)(factor0, factor1, product);
  input [(bitsize-1):0] factor0, factor1;
  output reg [((2*bitsize)-1):0] product;

  //Wires to carry signals between cells
  reg [bitsize-1:0] sum_vec   [bitsize:0];
  reg [bitsize-1:0] carry_vec [bitsize:0];

  //Inputs & Outputs of basecells
  reg [bitsize-1:0] f1_i   [bitsize:0];
  reg [bitsize-1:0] f2_i   [bitsize:0];
  reg [bitsize-1:0] b_i    [bitsize:0];
  reg [bitsize-1:0] c_i    [bitsize:0];
  wire [bitsize-1:0] sum_o [bitsize:0];
  wire [bitsize-1:0] c_o   [bitsize:0];

  integer i, j; //for rewiring loops
  genvar k, l;

  //Generate basecell modules
  generate
      for (k = 0; k < bitsize+1; k = k + 1) begin
          for (l = 0; l < bitsize; l = l + 1) begin : basecell
              basecell_fa bscll(f1_i[k][l], f2_i[k][l], b_i[k][l], c_i[k][l], sum_o[k][l], c_o[k][l]);
          end
      end
  endgenerate

  always@* begin
      //Wire renameing for basecell ports
      for(i = 0; i < bitsize+1; i = i + 1) begin
          for(j = 0; j < bitsize; j = j + 1) begin
              if(i != bitsize) begin
                  f1_i[i][j] = factor0[i];
                  f2_i[i][j] = factor1[j];
              end else begin
                  if(j == 0) begin
                      f1_i[i][j] = 1'b0;
                      f2_i[i][j] = 1'b0;
                  end else begin
                      f1_i[i][j] = carry_vec[i][j-1];
                      f2_i[i][j] = carry_vec[i][j-1];
                  end
              end

              if(i == 0) begin
                  b_i[i][j] = 1'b0;
              end else if(j == (bitsize - 1)) begin
                  b_i[i][j] = 1'b0;
              end else begin
                  b_i[i][j] = sum_vec[i-1][j+1];
              end

              if(i == 0) begin
                  c_i[i][j] = 1'b0;
              end else begin
                  c_i[i][j] = carry_vec[i-1][j];
              end

              sum_vec[i][j] = sum_o[i][j];
              
              carry_vec[i][j] = c_o[i][j];
          end
      end

      //Output wire renameing
      for(i = 0; i < bitsize+1; i = i + 1) begin
            product[i] = sum_vec[i][0];
      end
      for(i = 1; i < bitsize; i = i + 1) begin
            product[bitsize+i] = sum_vec[bitsize][i];
      end
      product[(2*bitsize)] = carry_vec[bitsize][bitsize-1];
  end

endmodule // Parameterized Carry Save Multiplier

module basecell_ha(f1_i, f2_i, b_i, sum_o, c_o);
  input f1_i, f2_i, b_i;
  output sum_o, c_o;

  wire pp;

  assign pp = f1_i & f2_i;

  HA adder(pp, b_i, sum_o, c_o);

endmodule // Base cell with half adder

module basecell_fa(f1_i, f2_i, b_i, c_i, sum_o, c_o);
  input f1_i, f2_i, b_i, c_i;
  output sum_o, c_o;

  wire pp;

  assign pp = f1_i & f2_i;

  FA adder(pp, b_i, c_i, sum_o, c_o);

endmodule // Base cell with full adder

//Simple 1 bit full adder
module FA(A, B, Cin, S, Cout);
  input A, B, Cin;
  output S, Cout;
  wire ha_sum; //Partial Sum without carry

  assign ha_sum = A ^ B;
  assign S =  ha_sum ^ Cin; //Sum
  assign Cout = (A & B) | (ha_sum & Cin); //Carry out
endmodule // full Adder

//Simple 1 bit half adder
module HA(A, B, S, Cout);
  input A, B;
  output S, Cout;

  assign S = A ^ B;
  assign Cout = A & B;
endmodule // half Adder