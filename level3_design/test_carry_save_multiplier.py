# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def random_testing(dut):
    
    error_message = []
    for i in range(1000):
        inp1= random.randint(0,255)
        inp2 = random.randint(0,255)
        expected_output = inp1 * inp2
        dut.factor0.value = inp1
        dut.factor1.value = inp2

        await Timer(1) 

        if(dut.product.value.integer != expected_output):
            msg = f'\nInp1:{hex(inp1)[2:].zfill(2)}.Inp2: {hex(inp2)[2:].zfill(2)}.Output:{hex(dut.product.value.integer)[2:].zfill(4)}.Expected Output:{hex(expected_output)[2:].zfill(4)}'
            error_message.append(msg)

    assert len(error_message) == 0, "Output not matching for following stimulus: {MSG}".format(MSG="".join(error_message))
            
@cocotb.test()
async def edge_case_testing(dut):

    error_message = []
    
    for test_scen in range(9):
        if(test_scen == 0):
            inp1 = 0
            inp2 = 0
        elif(test_scen == 1):
            inp1 = 255
            inp2 = 0
        elif (test_scen == 2):
            inp1 = 0
            inp2 = 255
        elif (test_scen == 3):
            inp1 = 255
            inp2 = 255
        elif (test_scen == 4):
            inp1 = 1
            inp2 = 1
        elif(test_scen == 5):
            inp1 = 255
            inp2 = 1
        elif(test_scen == 6):
            inp1 = 1
            inp2 = 255
        elif (test_scen == 7):
            inp1 = 128
            inp2 = 128
        
        dut.factor0.value = inp1
        dut.factor1.value = inp2
        expected_output = inp1 * inp2

        await Timer(1) 

        if(dut.product.value.integer != expected_output):
            msg = f'\nInp1:{hex(inp1)[2:].zfill(2)}.Inp2: {hex(inp2)[2:].zfill(2)}.Output:{hex(dut.product.value.integer)[2:].zfill(4)}.Expected Output:{hex(expected_output)[2:].zfill(4)}'
            error_message.append(msg)

    assert len(error_message) == 0, "Output not matching for following stimulus: {MSG}".format(MSG="".join(error_message))