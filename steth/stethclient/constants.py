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

import os
import socket
import sys
from netaddr import iter_iprange

from oslo_config import cfg
from steth.stethclient.utils import Logger


MGMT_TYPE = 'mgmt'
NET_TYPE = 'net'
STORAGE_TYPE = 'storage'
MGMT_AGENTS_CONFIG = {}
NET_AGENTS_CONFIG = {}
STORAGE_AGENTS_CONFIG = {}


OPTS = [
    cfg.StrOpt('node_name_prefix', default='server-',
               help="Prefix of every node."),
]

NEUTRON_CLIENT_OPTS = [
    cfg.StrOpt('username', default='admin',
               help='To get neutronclient, you must specify a username'),
    cfg.StrOpt('password', default='admin',
               help='To get neutronclient, you must specify a password'),
    cfg.StrOpt('tenant_name', default='admin',
               help='To get neutronclient, you must specify a project'),
    cfg.StrOpt('auth_url', default='http://127.0.0.1:5000/v2.0',
               help='To get neutronclient, you must specify a auth_url'),
]

mgmt_network_opts = [
    cfg.StrOpt('mgmt_ethernet_name',
               default='lo',
               help=("Name of managment ethernet name.")),
    cfg.StrOpt('mgmt_network_ranges',
               default='1.1.1.1:1.1.1.10',
               help=("String of <ip_addr_start>:<ip_addr_end> "
                     "tuples specifying the managment network.")),
]

sdn_network_opts = [
    cfg.StrOpt('sdn_ethernet_name',
               default='lo',
               help=("Name of sdn ethernet name.")),
    cfg.StrOpt('sdn_network_ranges',
               default='2.2.2.2:2.2.2.10',
               help=("String of <ip_addr_start>:<ip_addr_end> "
                     "tuples specifying the managment network.")),
]

storage_network_opts = [
    cfg.StrOpt('storage_ethernet_name',
               default='lo',
               help=("Name of storage ethernet name.")),
    cfg.StrOpt('storage_network_ranges',
               default='3.3.3.3:3.3.3.10',
               help=("String of <ip_addr_start>:<ip_addr_end> "
                     "tuples specifying the managment network.")),
]

cfg.CONF.register_opts(mgmt_network_opts, "mgmt_type_network")
cfg.CONF.register_opts(sdn_network_opts, "sdn_type_network")
cfg.CONF.register_opts(storage_network_opts, "storage_type_network")


ROOTDIR = os.path.dirname(__file__)
ETCDIR = os.path.join(ROOTDIR, '../', '../', 'etc')


def etcdir(*p):
    return os.path.join(ETCDIR, *p)


steth_config_file = etcdir('steth.conf')

cfg.CONF.register_opts(OPTS)
cfg.CONF.register_opts(NEUTRON_CLIENT_OPTS, 'neutron_client')

path_to_config_file = '/etc/steth/steth.conf'
if os.path.isfile(path_to_config_file):
    cfg.CONF([], project='steth',
             default_config_files=[path_to_config_file])
else:
    msg = ("There is no config file in this environment."
           "Please, create %s. Using sample config file now. "
           % path_to_config_file)
    Logger.log_high(msg)
    cfg.CONF([], project='steth',
             default_config_files=[steth_config_file])


MGMT_INTERFACE = cfg.CONF.mgmt_type_network.mgmt_ethernet_name
NET_INTERFACE = cfg.CONF.sdn_type_network.sdn_ethernet_name
STORAGE_INTERFACE = cfg.CONF.storage_type_network.storage_ethernet_name


def is_ip(addr):
    try:
        socket.inet_aton(addr)
        # valid
        return 0
    except socket.error:
        # invalid
        return 1


def get_ip_range(start, end):
    generator = iter_iprange(start, end, step=1)
    ips = []
    while True:
        try:
            ips.append(str(generator.next()))
        except StopIteration:
            break
    return ips


def program_exits_by_invalid_config():
    msg = ("Program exits because of invalid config.")
    Logger.log_high(msg)
    sys.exit()


def check_and_fill_info():
    infos = cfg.CONF.mgmt_type_network.mgmt_network_ranges
    if len(infos.split(':')) != 2:
        program_exits_by_invalid_config()
    start = infos.split(':')[0]
    end = infos.split(':')[1]
    if is_ip(start) or is_ip(end):
        program_exits_by_invalid_config()
    global MGMT_AGENTS_CONFIG
    MGMT_AGENTS_CONFIG = get_ip_range(start, end)


def check_and_fill_sdn_info():
    infos = cfg.CONF.sdn_type_network.sdn_network_ranges
    if len(infos.split(':')) != 2:
        program_exits_by_invalid_config()
    start = infos.split(':')[0]
    end = infos.split(':')[1]
    if is_ip(start) or is_ip(end):
        program_exits_by_invalid_config()
    global NET_AGENTS_CONFIG
    NET_AGENTS_CONFIG = get_ip_range(start, end)


def check_and_fill_storage_info():
    infos = cfg.CONF.storage_type_network.storage_network_ranges
    if len(infos.split(':')) != 2:
        program_exits_by_invalid_config()
    start = infos.split(':')[0]
    end = infos.split(':')[1]
    if is_ip(start) or is_ip(end):
        program_exits_by_invalid_config()
    global STORAGE_AGENTS_CONFIG
    STORAGE_AGENTS_CONFIG = get_ip_range(start, end)


def validate_and_parse_network_types():
    check_and_fill_info()
    check_and_fill_sdn_info()
    check_and_fill_storage_info()


validate_and_parse_network_types()
