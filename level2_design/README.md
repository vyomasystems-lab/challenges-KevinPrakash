# Sequence Detector Verification

![](https://github.com/vyomasystems-lab/challenges-KevinPrakash/blob/master/Capture.JPG)

## Verification Environment
 
The design is a bit manipulation processor. It takes 3 32 bit inputs (mav_putvalue_src1,mav_putvalue_src2,mav_putvalue_src3) and a 32 bit instruction (mav_putvalue_instr) and provides a 33 bit output mav_putvalue. 

 ## Test Scenario

### Test 1
Testing edge cases for input values
This is used to ensure that overflow and bit widths are specified correctly. 8 cases are present in this scenario. src1 is max, src2 is max, src3 is max, a combination of 2 srcs are max and a combination of 3 src are max. One random input sequence is passed to verify for all valid opcodes mentioned in the testing video.
The model.py file was modified to provide -1 for invalid opcodes so they can be diffrentiated from 0 value output. If the model output and dut output does not match then the test fails
            if((dut_output != expected_mav_putvalue) and (expected_mav_putvalue != -1)):
                error_messages.append(error_message)

### Test 2
Testing random opcodes and inputs
In this test 5000 random inputs are fed. This test was created to test scenarios which were not mentioned in the video incase it is a valid opcode.


## Test Output

### Test 1

                     Instr:40007033.Internal:00000000.Inp: ffffffff,00000000,00000000.Output:DUT:00000001 MODEL:1ffffffff
                     Instr:40007033.Internal:ffffffff.Inp: ffffffff,ffffffff,00000000.Output:DUT:1ffffffff MODEL:00000001
                     Instr:40007033.Internal:00000000.Inp: ffffffff,00000000,ffffffff.Output:DUT:00000001 MODEL:1ffffffff
                     Instr:40007033.Internal:ffffffff.Inp: ffffffff,ffffffff,ffffffff.Output:DUT:1ffffffff MODEL:00000001
                     Instr:40007033.Internal:80104505.Inp: 88b26755,f55dcd87,8c2688bc.Output:DUT:100208a0b MODEL:114444a1

                     A mask is applied to the instruction so that only the main bits are seen.

 ### Test 2

 AssertionError: 
                     Instr:40007033.Inp: 8adea800,e47bff5b,75da1e0e.Output:DUT:100b55001 MODEL:15080001
                     Instr:40007033.Inp: c9ad7706,0a5e4327,6a4b68a9.Output:DUT:1018860d MODEL:183426801
                     Instr:40007033.Inp: 4c1abfd5,dbc39d6b,ae319fc1.Output:DUT:90053a83 MODEL:08304529
                     Instr:40007033.Inp: 7887a51c,7f1e25a3,6f1ff75c.Output:DUT:f00c4a01 MODEL:01030039
                     Instr:40007033.Inp: 11507acb,54e39958,d19d5342.Output:DUT:20803091 MODEL:0220c507
                     Instr:40007033.Inp: f5e65ab2,a36ffc3b,123f999e.Output:DUT:142ccb065 MODEL:a9000501
                     Instr:40007033.Inp: f95f6ffa,3ac81885,17e97226.Output:DUT:70901101 MODEL:1822ecef5
                     Instr:40007033.Inp: 368d595d,06715eb6,4a98c9df.Output:DUT:0c02b029 MODEL:61180293
                     Instr:40007033.Inp: 095e2c31,ac64b9fc,0c1f72a8.Output:DUT:10885061 MODEL:02340803
                     Instr:40007033.Inp: 8bafea73,e5785471,b5247efa.Output:DUT:1025080e3 MODEL:150f5405
                     Instr:40007033.Inp: 220fca81,8b7eddc1,499bc421.Output:DUT:041d9103 MODEL:40020401


## Design Bugs

### Bug 1
Based on the output seen from the DUT and the model. It seems that the expected value is:
  (mav_putvalue_src1 & ~mav_putvalue_src2)<<1 + 1

But the dut output is just:
  (mav_putvalue_src1 & mav_putvalue_src2)<<1 + 1

## Design Fix

### Bug 1 Fix

Looking at the DUT source code we are passing mav_putvalue_src1 & mav_putvalue_src2 to x__h39889. This inturn is fed to the output which is the reason for the error.
The code has been corrected to pass mav_putvalue_src1 & ~mav_putvalue_src2 incase the istruction is 40xx7x33.
Original:   
assign x__h39889 = mav_putvalue_src1 & mav_putvalue_src2;
Fix:   
  assign temp1 = mav_putvalue_src1 & mav_putvalue_src2;
  assign temp2 = mav_putvalue_src1 & ~mav_putvalue_src2;
assign x__h39889 = (((mav_putvalue_instr[6:0] == 'b0110011)&&(mav_putvalue_instr[14:12] == 'b111)&&(mav_putvalue_instr[31:25] == 'b0100000))?temp2:temp1) ;

## Verification Stratergy

Due to the complex nature of the design, verification requires directed and random testing to achieve full verification.
Directed testing requires complete knowledge of the working of DUT. This can be used to check specific functionality and edge cases
Random testing can be used to verify general functionality.

## Is Verification complete

A large portion of functionality was tested but it is not possible to detect all the bugs with limited knowledge of DUT.
