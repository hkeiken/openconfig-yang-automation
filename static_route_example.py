#!/usr/bin/env python3
'''
Scipt that uses local routing openconfig yang model and inserts specific configuration.
The generate_binding.sh script is used to generate binding.py
'''
from __future__ import print_function, unicode_literals
from binding import openconfig_local_routing
import pyangbind.lib.pybindJSON as pybindJSON
import os

def write_file(filename,content):
    '''
    Function to write content to file
    '''
    file = open(filename, "w")
    file.write(content)
    file.close()

# Instantiate a copy of the pyangbind-kettle module
oclr = openconfig_local_routing()

# Add an entry to the static route list
rt = oclr.local_routes.static_routes.static.add("192.0.2.1/32")

# Add a set of next_hops
for nhop in [(0, "192.168.0.1"), (1, "10.0.0.1")]:
    nh = rt.next_hops.next_hop.add(nhop[0])
    nh.config.next_hop = nhop[1]

# Dump the static routes instance as JSON in IETF format
output = pybindJSON.dumps(oclr, mode="ietf")
write_file('openconfig-yang-json-output.txt',output)
print(output)
