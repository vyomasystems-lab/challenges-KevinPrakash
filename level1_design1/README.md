# MUX Verification

![] (https://github.com/vyomasystems-lab/challenges-KevinPrakash/blob/master/Capture.JPG)

## Verification Environment
 
The design is a MUX. It has 31 inputs, 1 select and 1 output pin. The select is a 5 bit signal which is used to decide which input pin value is available at the output. The test drives various inputs (inp0 - inp30 ,sel) and checks that the expected output is present.

 ## Test Scenario

Due to the small size of design we can run a test with every single input and verify the output is as expected.

inpi (where i is from 0-30) is a 2 bit signal. Hence it can take values from 0 to 3.
sel is a 5 bit signal and it can take values from 0 to 31.
Since only 31 inp singals are present the value 31 for sel is invalid and returns 0.

The assert statement ensures that the given inp value is available at the out port. error message is used to allow the test to run completly and capture all the failures before failing. 
    assert len(error_message) == 0, "Output not matching for following stimulus: {MSG}".format(MSG=error_message[:-1])

## Test Output

Errors found: AssertionError: Output not matching for following stimulus: (inp=1, out=0, sel=12),(inp=2, out=0, sel=12),(inp=3, out=0, sel=12),(inp=1, out=0, sel=13),(inp=2, out=0, sel=13),(inp=3, out=0, sel=13),(inp=1, out=0, sel=30),(inp=2, out=0, sel=30),(inp=3, out=0, sel=30)

## Design Bugs

### Bug 1
(inp=1, out=0, sel=12)

For sel value 12 the inp12 != out.
In the case statement, the sel value for inp 12 is 1101 ('d13) hence when sel = 12 the default case is choosen.

### Bug 2
(inp=1, out=0, sel=13)

For sel value 13 the inp13 != out.
In the case statement, the sel value for inp 13 is 1101 but the sel value for 12 is also 1101. Since they are priority based the first value is taken. Hence for sel = 13 inp12 is fed to out. 

### Bug 3
(inp=1, out=0, sel=30)

For sel value 30 the inp30 != out.
The value for inp30 is missing in the case statement hence for sel = 30 it is taking default value which is 0.

## Design Fix

### Bug 1 Fix

In the case statement, the sel value for inp 12 is 1101 ('d13) hence when sel = 12 the default case is choosen.
Fix is to change the value to 1100.

### Bug 2 Fix

In the case statement, the sel value for inp 13 is 1101 but the sel value for 12 is also 1101. Since they are priority based the first value is taken. Hence for sel = 13 inp12 is fed to out. 
Fix is to correct the sel value for inp12.

### Bug 3 Fix

The value for inp30 is missing in the case statement hence for sel = 30 it is taking default value which is 0.
Fix is to add 30 to case statement.

## Verification Stratergy

Due to the simple nature of the design, it is possible to feed every single input and test against every single output. 

## Is Verification complete

Verification is complete since every value of input and every value of output was tested. Additional testing would involve setting a value for every inp singal. Currently only the inp whose sel is set has a value assigned and the remaining are set to 0.
