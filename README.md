## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [How to use](#use)
* [Example of use](#example)
## General info

I got the quesion to show how to use yang to configure Junos.

Yang is a modeling language. For Networking, JunOS supports using
the OpenConfig Yang model for configuring switches. However,
Yang itself is the datamodel. For the modelling language to be
useful for JunOS, the data has to be converted to xml or json.
Most humans find json easier to the eyes than xml.

This set of tools is made to show how one can:
1. Use the OpenConfig Yang models
2. Update use them to generate a vendor neutral config
3. Save this config in json expression
4. Send this configuration, still vendor neutral to JunOS

This is a quick set of scripts to prove functions, not considered
a production ready script.

## Technologies
This collection of scripts uses Bash and Python3 as scripting languages. The Python libraries pyang and pyangbind is used to
collect the OpenConfig Yang models. The models are then instanciated
and used to generate a specific dataset. This dataset is then
stored as json. Finally PyEz is used to push the configuration to JunOS device.

vSRX with JunOS 20.1R1 was used in this example.

## Setup

First setup JunOS device. All JunOS devices since 18.3R1 has OpenConfig included, so there should be nothing else to install. There should be in config ssh, netconf ssh, netconf rfc-compliant and the hidden command to enable the OpenConfig schema.
```
set system services ssh
set system services netconf ssh
set system services netconf rfc-compliant
set system schema openconfig unhide
```

Then clone this github
```
git clone https://github.com/hkeiken/openconfig-yang-automation
```

Go into the directory:
```
cd openconfig-yang-automation
```

I prefer using Python virtual environments:
```
python3 -m venv ~/python-venv
source ~/python-venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

Set PYBINDPLUGIN constant:
```
export PYBINDPLUGIN=`/usr/bin/env python -c \
'import pyangbind; import os; print ("{}/plugin".format(os.path.dirname(pyangbind.__file__)))'`
```
Check that the constant is set:
```
echo $PYBINDPLUGIN
```

## How to use

Download OpenConfig models. This script downloads and build the
OpenConfig model that we will use later:
```
./generate_bindings.sh
```

Use the downloaded OpenConfig Yang model to generate a specific
configuration. This is generating a file openconfig-yang-json-output.txt file. If you have issues getting to this point,
there is an example file in openconfig-yang-json-output-example.txt
that can be used to push configuration to JunOS device.
```
 ./static_route_example.py
```

Then one will push this configuration to JunOS device:
```
./push_config.py 172.16.75.142 username password openconfig-yang-json-output.txt
```

## Example of use

Generate config in json:
```
(python-venv) user@user openconfig-yang-automation % ./static_route_example.py
{
    "openconfig-local-routing:local-routes": {
        "static-routes": {
            "static": [
                {
                    "prefix": "192.0.2.1/32",
                    "next-hops": {
                        "next-hop": [
                            {
                                "index": "0",
                                "config": {
                                    "next-hop": "192.168.0.1"
                                }
                            },
                            {
                                "index": "1",
                                "config": {
                                    "next-hop": "10.0.0.1"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}
```

Then the json openconfig is sent to JunOS device:
```
(python-venv) user@user openconfig-yang-automation % ./push_config.py 192.168.1.2 user password openconfig-yang-json-output.txt
{
"configuration" : {
    "openconfig-local-routing:local-routes": {
        "static-routes": {
            "static": [
                {
                    "prefix": "192.0.2.1/32",
                    "next-hops": {
                        "next-hop": [
                            {
                                "index": "0",
                                "config": {
                                    "next-hop": "192.168.0.1"
                                }
                            },
                            {
                                "index": "1",
                                "config": {
                                    "next-hop": "10.0.0.1"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}
}
Sending configuration to 192.168.1.2
```

Then this configuration is activated in JunOS:
```
root@vsrx> show configuration openconfig-local-routing:local-routes
static-routes {
    static 192.0.2.1/32 {
        next-hops {
            next-hop 0 {
                config {
                    next-hop 192.168.0.1;
                }
            }
            next-hop 1 {
                config {
                    next-hop 10.0.0.1;
                }
            }
        }
    }
}
```

One can also see the translated JunOS config if wanted:
```
root@vsrx-> show configuration | display translation-scripts translated-config
routing-options {
    static {
        route 192.0.2.1/32 next-hop [ 192.168.0.1 10.0.0.1 ];
    }
}
```
