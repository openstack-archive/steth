..
      Copyright 2011-2016 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Welcome to Steth's developer documentation!
===========================================

Steth is an inspection tool that can aid in pinpointing issues before deployment and during operation of an OpenStack environment.


Quick start
===========
Steth is a network inspection tool for OpenStack.

It is modelled as agent(s)/client in which a controller interacts with
agents deployed in your environment. Let me introduce how to use steth.

Download code
-------------

Download the latest code from git repository. And run `python setup.py install`
to install steth. After running that, you can `steth - -help` to confirm Steth
is installed correctly.


Deploy Steth Agent
------------------

Steth Agent listens in 0.0.0.0:9698 on any node you want. It will wait for
RPC request. Currently we support CentOS 6.5, CentOS 7.0 and CentOS 7.1 only.
In CentOS 6.5, you should run `service steth-agent start` to start steth-agent.
In CentOS 7.0 and 7.1, you should run `systemctl start steth` to start steth-agent.

Deploy Steth Client
-------------------

Steth Client is a stateless program. You can run `steth - -help` to show all steth
commands that you can run.

Configuration File
---------------------

On start the client will read a configuration file. By default the configuration file is located at /etc/steth/steth.conf.
Here is an example about the configuration file: ::

 # (ListOpt) list of networks types.
 # We may have multi network types in one node, such as mgmt, net and stroage.
 # so this value should be a list.
 # We seperate each item by ":". Treat first item as network type.
 # The second is physical nic name. And the third is network_prefix.
 # Example: "mgmt:eth0:1.1.1.,net:eth1:2.2.2.,storage:eth2:3.3.3."
 network_types=mgmt:eth0:1.1.1.,net:eth1:2.2.2.,storage:eth2:3.3.3.

 # (ListOpt) All nodes info. Just need sequence number.
 # Example: 64, 65, 66
 nodes_id=39,233,64,65,66

 # (StrOpt) Name prefix of every node. By default, this value
 # is "server". We combine "node_name_prefix" with
 # "nodes_id", to define nodes. Such as "server-64", "server-68"
 # and so on. In every region, we give every node a specific name.
 # Ensure that DNS can resolve the nodes.
 node_name_prefix=server-
