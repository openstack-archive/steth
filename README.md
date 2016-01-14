# Stetho
[![Build Status](https://travis-ci.org/unitedstack/stetho.svg?branch=master)](https://travis-ci.org/unitedstack/stetho)

A network inspection tool for OpenStack.

Stetho is an inspection tool that can aid in pinpointing issues before deployment and during operation of an OpenStack environment.

It is modelled as agent(s)/client in which a controller interacts with agents deployed in your environment.

## Background

OpenStck networking can be deloyed as different architecture such as ml2 with ovs(legacy and dvr), linux bridge, ovn, dragonflow and more. But they both need some enviroment prerequisites such as vlan is configure as we expect, bandwidth match our need, connection between nodes are active.

Besides, with some well-deployed architecture, check problem of vm networking is pretty difficult, like why vm can not get ip address, why it can't connect to Internet, etc. Stetho intergates some useful scripts or 3rd tools(like iperf, tcpdump, etc) to help operator track vm ntwork.

## Mission

Stetho is just like a self-checking tool for openstack networking, work in ml2 with ovs will maximize the effects for now.Stetho is just like a self-checking tool for openstack networking, 


## Multiple Node Architecture

```
                                                                       note that stetho will not save any state,
                                                                       it just like a rpc client to make request
                                                                       to stetho agent and analyse result.
                                    +--------------------------+
                                    |                          |
                                    |   +----CLI-----------+   |
                                    |   |                  |   |
             +--------------------------+    stetho        +--------------------------+
             |                      |   |                  |   |                      |
             |                      |   +--------+---------+   |                      |
             |                      |            |             |                      |
             |                      +--------------------------+                      |
             |                                   |                                    |
             v                                   v                                    v
+-------+port:9698---------+        +-------+port:9698---------+         +-------+port:9698---------+
|            ^             |        |            ^             |         |            ^             |
|            |             |        |            |             |         |            |             |
| +----------+-------+     |        | +----------+-------+     |         | +----------+-------+     |
| |                  |     |        | |                  |     |         | |                  |     |
| |  stetho-agent    |     |        | |  stetho-agent    |     |         | |  stetho-agent    |     |
| |                  |     |        | |                  |     |         | |                  |     |
| +-----------+------+     |        | +-----------+------+     |         | +-----------+------+     |
|             |            |        |             |            |         |             |            |
|             |            |        |             |            |         |             |            |
|  +----------v----------+ |        |  +----------v----------+ |         |  +----------v----------+ |
|  | run command like:   | |        |  | run command like:   | |         |  | run command like:   | |
|  | ping, iperf, tcpdump| |        |  | ping, iperf, tcpdump| |         |  | ping, iperf, tcpdump| |
|  +---------------------+ |        |  +---------------------+ |         |  +---------------------+ |
|                          |        |                          |         |                          |
|                          |        |                          |         |                          |
+--------------------------+        +--------------------------+         +--------------------------+
```

In multiple nodes scenario, Stetho is a non-state cli and controller, it know location of eech stetho agent and will read config, interfact with openstack then downcall agents which need. 

Stetho Agent is introduced to manage process or run command. Stetho agent should be installed in each compute and network node, and there IPs shoud be defined at config file.

## Stetho Agent

Linstening in 0.0.0.0:9698 waiting for rpc request.

Note: for get_interface() agent api, we use ifconfig to get complete information. But output of ifconfig varies from a linux distribution to another, the api has been tested on centos 6.5 and 7.0, and not for any other distributions.
