#!/usr/bin/python
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


import random
import sys

from oslo_config import cfg

try:
    from neutronclient.v2_0 import client
    from neutronclient.common import exceptions
except ImportError:
    print "Import neutronclient error. Please check it out."
    sys.exit()


def get_neutronclient():
    neutroncli = client.Client(
        username=cfg.CONF.neutron_client.username,
        password=cfg.CONF.neutron_client.password,
        tenant_name=cfg.CONF.neutron_client.tenant_name,
        auth_url=cfg.CONF.neutron_client.auth_url)
    return neutroncli


def get_port_attr(port_id, attr):
    client = get_neutronclient()
    try:
        res = client.show_port(port_id)
    except exceptions.NeutronClientException:
        print 'Port %s Not Found.' % port_id
        return
    except KeyError:
        print 'Port attr: %s Not Found.' % attr
        return

    return res['port'][attr]


def choose_one_network_agent(network_id):
    client = get_neutronclient()
    dhcp_agents = client.list_dhcp_agent_hosting_networks(network_id)
    return random.choice(dhcp_agents['agents'])['host']
