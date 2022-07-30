# Sequence Detector Verification

![](https://github.com/vyomasystems-lab/challenges-KevinPrakash/blob/master/Capture.JPG)

## Verification Environment
 
The design is a 1011 sequence detector. The design has 3 inputs(inp_bit, clk,reset) and one output seq_seen. When the sequence is seen the output will be asserted for one clock cycle. The reset signal is used to reset the internal state machine. The design is an overlapping sequence detector, so it is supposed to retain internal state if partial sequence is detected.

 ## Test Scenario

### Test 1
Testing random input and random reset assertion.
For 5000 clock cycles a random inp_bit signal is fed and a 10% probability on reset is set. The test retains the last 8 values for debug purpose and checks if the sequence is present in the previous 4 inp_bits. If the signal was present and seq_seen is not asserted then the sequence is stored, similarly if seq_seen is asserted but the sequence was not present then the sequence is stored.
At the end of the test the failing sequences are printed
        if((previous_inp[-4:] == sequence) and (dut.seq_seen.value == 0)):
                failed_stimulus.append(error_message)

The test also checks if seq_seen is asserted for 3 clock cycles after a reset is given.
                if(dut.seq_seen.value == 1): assert (i - prev_reset > 3), "Sequence is detected even after reset for stimulus: {MSG},reset at:{SL}".format(MSG=",".join(failed_stimulus),SL=str(prev_reset-i))

### Test 2
Testing overlap situations
A total of 4 sequences is tested with different levels of overlap, to ensure that overlapping is tested throughly.
            if((input_feed[inp-3:inp+1] == sequence) and (dut.seq_seen.value != 1)):
                failed_sequence.append(",".join(input_feed[:inp+1]))


## Test Output

### Test 1

AssertionError: Output not matching for following stimulus: 000001011,010011011,101001011,010001011,000111011,110001011,001011011,011001011,001111011,011111011,101111011,100111011,001101011,010111011,111011011,011011011,000011011,000101011,011101011,010101011,110011011,101101011,001001011,111001011,100101011,111111011,100001011,101011011,100011011,110111011,110101011,111101011

 ### Test 2

AssertionError: Output(1) not recieved for overlapping sequence: 1,0,1,1,0,1,1

## Design Bugs

### Bug 1
Chain of 1 is not detecting sequence correctly

### Bug 2
Input of 1010 is prior to sequence is not detecting correctly


### Bug 3
Overlap is not getting detected

## Design Fix

### Bug 1 Fix

Chain of 1 is not detecting sequence correctly.
In the state machine, for SEQ_1 if inp_bit is 1 then it should remain in SEQ_1 state.

### Bug 2 Fix

Input of 1010 is prior to sequence is not detecting correctly
In the state machine, for SEQ_101 when inp_bit is 0 it should go to SEQ_10 state.

### Bug 3 Fix

Input of 1011 followed by 011 is not getting detected.
In the state machine for SEQ_1011 when inp_bit is 1 it should go to SEQ_1. If inp_bit is 0 it should go to SEQ_10.

## Verification Stratergy

Due to the simple nature of the design, it is possible to feed every single input and test against every single output. 

## Is Verification complete

Verification is complete since every value of input and every value of output was tested. Additional testing would involve setting a value for every inp singal. Currently only the inp whose sel is set has a value assigned and the remaining are set to 0.
