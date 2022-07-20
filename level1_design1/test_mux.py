# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    SEL_BITS = 5
    IN_BITS = 2

    for sel in range(0,2**SEL_BITS):
        for val in range(0,2**IN_BITS):
            dut.sel.value = sel
            exec("dut.%s.value = %d" % (("inp"+str(sel)),val))

            await Timer(1,units="ns")
   
            if(dut.out.value != val):
              print("Mux output is incorrect. Expected:{EXP},Obtained:{OBT} for sel:{SEL}".format(EXP=val,OBT=dut.out.value.integer,SEL=sel))
              
            exec("dut.%s.value = %d" % (("inp"+str(sel)),0))
            
    cocotb.log.info('##### CTB: Develop your test here ########')

