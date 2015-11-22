# -*- coding: utf-8 -*-
# Copyright (c) 2015 Mark D. Hill and David A. Wood
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Jason Power

# This file creates a simple system with a single CPU and a 2-level cache
# and executes 'hello', a simple Hello World application.
#
# This config file assumes that the x86 ISA was built

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *

# parser
import os,optparse,sys

# SPEC06
import spec06_benchmarks

# import the caches which we made
from rrip_lab_cache import *

parser = optparse.OptionParser()
parser.add_option("-b", "--benchmark", type="string", default="", help="The SPEC benchmark to be loaded.")
parser.add_option("--benchmark_stdout", type="string", default="", help="Absolute path for stdout redirection for the benchmark.")
parser.add_option("--benchmark_stderr", type="string", default="", help="Absolute path for stderr redirection for the benchmark.")

(options, args) = parser.parse_args()

if options.benchmark:
    print 'Selected SPEC_CPU2006 benchmark'
    if options.benchmark == 'perlbench':
        print '--> perlbench'
        process = spec06_benchmarks.perlbench
    elif options.benchmark == 'bzip2':
        print '--> bzip2'
        process = spec06_benchmarks.bzip2
    elif options.benchmark == 'gcc':
        print '--> gcc'
        process = spec06_benchmarks.gcc
    elif options.benchmark == 'bwaves':
        print '--> bwaves'
        process = spec06_benchmarks.bwaves
    elif options.benchmark == 'gamess':
        print '--> gamess'
        process = spec06_benchmarks.gamess
    elif options.benchmark == 'mcf':
        print '--> mcf'
        process = spec06_benchmarks.mcf
    elif options.benchmark == 'milc':
        print '--> milc'
        process = spec06_benchmarks.milc
    elif options.benchmark == 'zeusmp':
        print '--> zeusmp'
        process = spec06_benchmarks.zeusmp
    elif options.benchmark == 'gromacs':
        print '--> gromacs'
        process = spec06_benchmarks.gromacs
    elif options.benchmark == 'cactusADM':
        print '--> cactusADM'
        process = spec06_benchmarks.cactusADM
    elif options.benchmark == 'leslie3d':
        print '--> leslie3d'
        process = spec06_benchmarks.leslie3d
    elif options.benchmark == 'namd':
        print '--> namd'
        process = spec06_benchmarks.namd
    elif options.benchmark == 'gobmk':
        print '--> gobmk'
        process = spec06_benchmarks.gobmk
    elif options.benchmark == 'dealII':
        print '--> dealII'
        process = spec06_benchmarks.dealII
    elif options.benchmark == 'soplex':
        print '--> soplex'
        process = spec06_benchmarks.soplex
    elif options.benchmark == 'povray':
        print '--> povray'
        process = spec06_benchmarks.povray
    elif options.benchmark == 'calculix':
        print '--> calculix'
        process = spec06_benchmarks.calculix
    elif options.benchmark == 'hmmer':
        print '--> hmmer'
        process = spec06_benchmarks.hmmer
    elif options.benchmark == 'sjeng':
        print '--> sjeng'
        process = spec06_benchmarks.sjeng
    elif options.benchmark == 'GemsFDTD':
        print '--> GemsFDTD'
        process = spec06_benchmarks.GemsFDTD
    elif options.benchmark == 'libquantum':
        print '--> libquantum'
        process = spec06_benchmarks.libquantum
    elif options.benchmark == 'h264ref':
        print '--> h264ref'
        process = spec06_benchmarks.h264ref
    elif options.benchmark == 'tonto':
        print '--> tonto'
        process = spec06_benchmarks.tonto
    elif options.benchmark == 'lbm':
        print '--> lbm'
        process = spec06_benchmarks.lbm
    elif options.benchmark == 'omnetpp':
        print '--> omnetpp'
        process = spec06_benchmarks.omnetpp
    elif options.benchmark == 'astar':
        print '--> astar'
        process = spec06_benchmarks.astar
    elif options.benchmark == 'wrf':
        print '--> wrf'
        process = spec06_benchmarks.wrf
    elif options.benchmark == 'sphinx3':
        print '--> sphinx3'
        process = spec06_benchmarks.sphinx3
    elif options.benchmark == 'xalancbmk':
        print '--> xalancbmk'
        process = spec06_benchmarks.xalancbmk
    elif options.benchmark == 'specrand_i':
        print '--> specrand_i'
        process = spec06_benchmarks.specrand_i
    elif options.benchmark == 'specrand_f':
        print '--> specrand_f'
        process = spec06_benchmarks.specrand_f
    else:
        print "No recognized SPEC2006 benchmark selected! Exiting."
        sys.exit(1)
else:
    print >> sys.stderr, "Need --benchmark switch to specify SPEC CPU2006 workload. Exiting!\n"
    sys.exit(1)
 
# Set process stdout/stderr
if options.benchmark_stdout:
    process.output = options.benchmark_stdout
    print "Process stdout file: " + process.output
if options.benchmark_stderr:
    process.errout = options.benchmark_stderr
    print "Process stderr file: " + process.errout

# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('4096MB')] # Create an address range

# Create a simple CPU
system.cpu = TimingSimpleCPU()

# Create an L1 instruction and data cache
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu.icache_port)
system.cpu.dcache.connectCPU(system.cpu.dcache_port)

# Create a memory bus, a coherent crossbar, in this case
system.l2bus = CoherentXBar()

# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create an L2 cache and connect it to the l2bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

# Create a memory bus
system.membus = CoherentXBar()

# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)

# create the interrupt controller for the CPU and connect to the membus
# Note: these are directly connected to the memory bus and are not cached
system.cpu.createInterruptController()
system.cpu.interrupts.pio = system.membus.master
system.cpu.interrupts.int_master = system.membus.slave
system.cpu.interrupts.int_slave = system.membus.master

# Connect the system up to the membus
system.system_port = system.membus.slave

# Create a DDR3 memory controller
system.mem_ctrl = DDR3_1600_x64()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print "Beginning simulation!"
exit_event = m5.simulate()
print 'Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause())

