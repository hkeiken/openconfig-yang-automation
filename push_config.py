#!/usr/bin/env python3
'''
Simple program to send content of a file to junos device
The program expect the content of file to be set commands
'''
import sys
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConfigLoadError,CommitError

def read_file_content(filename):
    '''
    Function to read file content
    '''
    f = open(filename)
    output = f.read()
    f.close()
    return output

def send_config_to_device(device_name,username,password,configuration):
    '''
    Function to send content of configuration file to device
    '''
    print("Sending configuration to "+device_name)
    dev = Device(host=device_name, user=username, password=password, gather_facts=False)
    dev.open()
    with Config(dev, mode='private') as cu:
        try:
            cu.load(configuration, merge=True)
            cu.commit(comment='Programatical commit with 2 minutes timeout.',confirm=2)
            cu.commit_check()
        except (ConfigLoadError,CommitError) as err:
            print(err)
            cu.rollback()

if __name__ == "__main__":
        #Reading attributes
    if len(sys.argv) == 4+1:
        host = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        configfile = sys.argv[4]
        config = read_file_content(configfile)
        config_junos = "{{\n\"configuration\" : {0}\n}}".format(config)
        print(config_junos)
        send_config_to_device(host,username,password,config_junos)
    else:
        print("Wrong number of arguments")
