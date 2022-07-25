# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

export PYTHONPATH := $(PWD):$(PYTHONPATH)            # provide your design path

VERILOG_SOURCES = $(PWD)/carry_save_multiplier.v

TOPLEVEL := csmulti_fullbasecell        # design file
MODULE   := test_carry_save_multiplier   # test file

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 
