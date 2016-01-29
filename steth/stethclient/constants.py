# Copyright 2015 UnitedStack, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import socket
import sys
from oslo_config import cfg

OPTS = [
    cfg.ListOpt('network_types', default=[],
                help="Mappings of network types and prefix of networks."),
    cfg.ListOpt('nodes_id', default=[],
                help="List of nodes."),
    cfg.StrOpt('node_name_prefix', default='server-',
               help="Prefix of every node."),
]

cfg.CONF.register_opts(OPTS)
cfg.CONF([], project='steth',
         default_config_files=['/etc/steth/steth.conf'])

MGMT_AGENTS_INFOS = {}
NET_AGENTS_INFOS = {}
STORAGE_AGENTS_INFOS = {}

MGMT_TYPE = 'mgmt'
NET_TYPE = 'net'
STORAGE_TYPE = 'storage'

MGMT_INTERFACE = None
NET_INTERFACE = None
STORAGE_INTERFACE = None


def is_ip(addr):
    try:
        socket.inet_aton(addr)
        # valid
        return 0
    except socket.error:
        # invalid
        return 1


def check_ip_and_fill(agent_type, net_prefix):
    d = {}
    name_prefix = cfg.CONF.node_name_prefix
    for node in cfg.CONF.nodes_id:
        if not is_ip(net_prefix + node):
            d[name_prefix + node] = net_prefix + node
            agent_type.update(d)
        else:
            print "%s is not IP!" % name_prefix + node


def validate_and_parse_network_types():
    if not cfg.CONF.network_types:
        print 'You must fill network_types in config file!'
        sys.exit()
    for network_type in cfg.CONF.network_types:
        net_type, net_interface, net_prefix = network_type.split(':')
        # parse mgmt networks
        if net_type == MGMT_TYPE:
            check_ip_and_fill(MGMT_AGENTS_INFOS, net_prefix)
            global MGMT_INTERFACE
            MGMT_INTERFACE = net_interface
        # parse net networks
        elif net_type == NET_TYPE:
            check_ip_and_fill(NET_AGENTS_INFOS, net_prefix)
            global NET_INTERFACE
            NET_INTERFACE = net_interface
        # parse stor networks
        elif net_type == STORAGE_TYPE:
            check_ip_and_fill(STORAGE_AGENTS_INFOS, net_prefix)
            global STORAGE_INTERFACE
            STORAGE_INTERFACE = net_interface
        else:
            print "Unkown network_types: %s" % network_type
