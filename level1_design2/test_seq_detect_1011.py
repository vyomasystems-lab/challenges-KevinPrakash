# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_random_inp_and_reset(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    previous_inp = [0,0,0,0,0,0,0,0]
    sequence = [1,0,1,1]

    failed_stimulus = []
    prev_reset = 0


    for i in range(5000):
        inp = random.randint(0,1)
        previous_inp.append(inp)
        dut.inp_bit.value = inp

        if(random.randint(0,10) == 0): # 10 % percent probability for reset
            for i in range(len(previous_inp)):
                previous_inp[i] = 0
            dut.reset.value = 1
            prev_reset = i


        await Timer(10,units="us")

        dut.reset.value = 0 # clearing reset after one clk cycle


        if((previous_inp[-4:] == sequence) and (dut.seq_seen.value == 0)):
            error_message = ""
            for i in previous_inp:
                error_message = error_message + str(i)
            if error_message not in failed_stimulus:
                failed_stimulus.append(error_message)

        
        if(dut.seq_seen.value == 1): assert (i - prev_reset > 3), "Sequence is detected even after reset for stimulus: {MSG},reset at:{SL}".format(MSG=",".join(failed_stimulus),SL=str(prev_reset-i))


        previous_inp = previous_inp[1:]
    
    assert len(failed_stimulus) == 0, "Output not matching for following stimulus: {MSG}".format(MSG=",".join(failed_stimulus))
    


@cocotb.test()
async def test_fixed_inp_overlap(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    sequence = ["1","0","1","1"]
    failed_stimulus = []

    for i in range(1,len(sequence)):
        # reset
        dut.reset.value = 1
        await FallingEdge(dut.clk)  
        dut.reset.value = 0
        await FallingEdge(dut.clk)

        input_feed = sequence[:i] + sequence
        failed_sequence = []

        for inp in range(len(input_feed)):
            dut.inp_bit.value = int(input_feed[inp])
            #await FallingEdge(dut.clk)
            await Timer(10,units="us")
            if((input_feed[inp-3:inp+1] == sequence) and (dut.seq_seen.value != 1)):
                failed_sequence.append(",".join(input_feed[:inp+1]))
    assert (len(failed_sequence) == 0), "Output(1) not recieved for overlapping sequence: {MSG}".format(MSG="|".join(failed_sequence)) 
