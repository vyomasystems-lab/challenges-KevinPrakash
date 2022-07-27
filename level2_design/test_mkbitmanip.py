# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_edge_case_testing(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    valid_opcodes = [[0,7,51],[0,6,51],[0,4,51],[32,7,51],[32,6,51],[32,4,51],[0,1,51],[0,5,51],[32,5,51],[16,1,51],[16,5,51],[48,1,51],[48,5,51],[36,1,51],[20,1,51],[52,1,51]\
    ,[36,5,51],[20,5,51],[52,5,51],[0,1,19],[0,5,19],[32,5,19],[16,1,19],[16,5,19],[48,5,19],[36,1,19],[20,1,19],[52,1,19],[36,5,19],[20,5,19],[52,5,19]]

    error_messages = []
    for opcode in valid_opcodes:
    ######### CTB : Modify the test to expose the bug #############
    # input transaction
        for test_scen in range(0,9):
            if(test_scen == 0):
                mav_putvalue_src1 = 0
                mav_putvalue_src2 = 0
                mav_putvalue_src3 = 0
            elif(test_scen == 1):
                mav_putvalue_src1 = 4294967295
                mav_putvalue_src2 = 0
                mav_putvalue_src3 = 0
            elif(test_scen == 2):
                mav_putvalue_src1 = 0
                mav_putvalue_src2 = 4294967295
                mav_putvalue_src3 = 0
            elif(test_scen == 3):
                mav_putvalue_src1 = 0
                mav_putvalue_src2 = 0
                mav_putvalue_src3 = 4294967295
            elif(test_scen == 4):
                mav_putvalue_src1 = 4294967295
                mav_putvalue_src2 = 4294967295
                mav_putvalue_src3 = 0
            elif(test_scen == 5):
                mav_putvalue_src1 = 4294967295
                mav_putvalue_src2 = 0
                mav_putvalue_src3 = 4294967295
            elif(test_scen == 6):
                mav_putvalue_src1 = 0
                mav_putvalue_src2 = 4294967295
                mav_putvalue_src3 = 4294967295
            elif(test_scen == 7):
                mav_putvalue_src1 = 4294967295
                mav_putvalue_src2 = 4294967295
                mav_putvalue_src3 = 4294967295
            elif(test_scen == 8):
                mav_putvalue_src1 = random.randint(1,4294967295)
                mav_putvalue_src2 = random.randint(1,4294967295)
                mav_putvalue_src3 = random.randint(1,4294967295)

            mav_putvalue_instr = 4294967295 & ((opcode[0] << 25 ) | (random.randint(0,1023) << 15 ) | (opcode[1] << 12 ) | (random.randint(0,31) << 7) | (opcode[2]))

            # expected output from the model
            expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

            # driving the input transaction
            dut.mav_putvalue_src1.value = mav_putvalue_src1
            dut.mav_putvalue_src2.value = mav_putvalue_src2
            dut.mav_putvalue_src3.value = mav_putvalue_src3
            dut.EN_mav_putvalue.value = 1
            dut.mav_putvalue_instr.value = mav_putvalue_instr
  
            yield Timer(1) 

            # obtaining the output
            dut_output = dut.mav_putvalue.value

            #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
            #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
            # comparison
            error_message = f'\nInstr:{hex(mav_putvalue_instr)[2:].zfill(8)}.Inp: {hex(mav_putvalue_src1)[2:].zfill(8)},{hex(mav_putvalue_src2)[2:].zfill(8)},{hex(mav_putvalue_src3)[2:].zfill(8)}.Output:DUT:{hex(dut_output)[2:].zfill(8)} MODEL:{hex(expected_mav_putvalue)[2:].zfill(8)}'
            if((dut_output != expected_mav_putvalue) and (expected_mav_putvalue != -1)):
                error_messages.append(error_message)

    assert len(error_messages) == 0, "".join(error_messages)

# Sample Test
@cocotb.test()
def run_random_testing(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    error_messages = []

 

    for i in range(0,10000):
        expected_mav_putvalue = 0
        while(expected_mav_putvalue == -1):
            mav_putvalue_src1 = random.randint(0,4294967295)
            mav_putvalue_src2 = random.randint(0,4294967295)
            mav_putvalue_src3 = random.randint(0,4294967295)
            mav_putvalue_instr = random.randint(0,4294967295)
            expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
        

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
  
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
        # comparison
        error_message = f'\nInstr:{hex(mav_putvalue_instr)[2:].zfill(8)}.Inp: {hex(mav_putvalue_src1)[2:].zfill(8)},{hex(mav_putvalue_src2)[2:].zfill(8)},{hex(mav_putvalue_src3)[2:].zfill(8)}.Output:DUT:{hex(dut_output)[2:].zfill(8)} MODEL:{hex(expected_mav_putvalue)[2:].zfill(8)}'
        if(dut_output != expected_mav_putvalue):
            error_messages.append(error_message)

    assert len(error_messages) == 0, "".join(error_messages)