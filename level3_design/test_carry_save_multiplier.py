# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    
    dut.factor0.value = 5
    dut.factor1.value = 8

    await Timer(1) 

    print(str(dut.factor0.value.integer) +" x " + str(dut.factor1.value.integer) + " = " + str(dut.product.value.integer))
    #assert len(error_message) == 0, "Output not matching for following stimulus: {MSG}".format(MSG=error_message[:-1])
            
    cocotb.log.info('##### CTB: Develop your test here ########')