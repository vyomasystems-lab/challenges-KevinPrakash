# Sequence Detector Verification

![](https://github.com/vyomasystems-lab/challenges-KevinPrakash/blob/master/Capture.JPG)

## Verification Environment
 
This design is a 8 bit unsigned multiplier using carry save adder. This design supports 2 8 bit inputs (factor0 and factor1) and one 16 bit output (product).

 ## Test Scenario

### Test 1
Testing random input
For 5000 cycles random input is provided and the output is checked to see it matches with expected value.
        if(dut.product.value.integer != expected_output):
            msg = f'\nInp1:{hex(inp1)[2:].zfill(2)}.Inp2: {hex(inp2)[2:].zfill(2)}.Output:{hex(dut.product.value.integer)[2:].zfill(4)}.Expected Output:{hex(expected_output)[2:].zfill(4)}'
            error_message.append(msg)

### Test 2
Testing edge case values
This is used to ensure that the upper bits and overflow is handled correctly. 
        if(dut.product.value.integer != expected_output):
            msg = f'\nInp1:{hex(inp1)[2:].zfill(2)}.Inp2: {hex(inp2)[2:].zfill(2)}.Output:{hex(dut.product.value.integer)[2:].zfill(4)}.Expected Output:{hex(expected_output)[2:].zfill(4)}'
            error_message.append(msg)

## Design Bugs

### Bug 1
index mismatch.f2_1[i][j] = factor1[i].
This will create a transposed array which will result in totally different answer unless the values are mirrored. ie inputs like 0 or ff.

### Bug 2
carry_vec[bitsize-1][bitsize-1]
The MSB of product has incorrect value. This will be caught only when the product is large enough

### Bug 3
f1_i | f2_i
The bits of input are ORed instead of ANDed. This will result in sum instead of product again this will not affect numbers where both bits are 0 or both bits are 1.

## Verification Stratergy

Due to the simple nature of the design, it is possible to feed every single input and test against every single output.

## Is Verification complete

Yes, no other form of testing is possible
