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

import logging
import sys

from cliff.lister import Lister
from steth.stethclient.clients import neutron
from steth.stethclient import utils


class CheckDHCPonComputeNodes(Lister):
    "Check DHCP on compute nodes."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckDHCPonComputeNodes, self).get_parser(prog_name)
        parser.add_argument('port_id', default='bad',
                            help='ID of port to look up.')
        parser.add_argument('physical_interface', default='bad',
                            help=('Name of physical interface.'
                                  'We catch packets at this interface'))
        parser.add_argument('network_type', default='vlan',
                            help='Network type, you want to check.')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        if not utils.is_uuid_like(parsed_args.port_id):
            utils.Logger.log_fail("Port id: %s is not like"
                                  "uuid." % parsed_args.port_id)
            sys.exit()
        # get network_type
        network_type = parsed_args.network_type
        if network_type != 'vlan' and network_type != 'vxlan':
            utils.Logger.log_fail("Network type %s not support!"
                                  "Please choose from 'vlan' and 'vxlan'."
                                  % network_type)
            sys.exit()
        self.log.debug("network_type is %s" % network_type)

        # get port's address
        port_mac_address = neutron.get_port_attr(parsed_args.port_id,
                                                 'mac_address')
        if not port_mac_address:
            utils.Logger.log_fail("Get port mac_address fails."
                                  "Please check this port.")
            sys.exit()
        self.log.debug("port mac address is %s" % port_mac_address)

        # get port's host info
        host_id = neutron.get_port_attr(parsed_args.port_id, 'binding:host_id')
        if not host_id:
            utils.Logger.log_fail("Port %s doesn't attach to any vms."
                                  % parsed_args.port_id)
            sys.exit()
        self.log.debug("port host id is %s" % host_id)

        # setup steth server
        try:
            server = utils.setup_server(host_id)
            self.log.debug("setup server: %s" % host_id)
        except:
            utils.Logger.log_fail("Setup server fail in: %s." % server)
            sys.exit()

        # get physical interface name
        physical_interface = parsed_args.physical_interface
        self.log.debug("Physical interface is %s" % physical_interface)

        res = server.check_dhcp_on_comp(port_id=parsed_args.port_id,
                                        port_mac=port_mac_address,
                                        phy_iface=physical_interface,
                                        net_type=network_type)
        self.log.debug("Response is %s" % res)
        data = res['data']
        return (['Device Name', 'Result'],
                (['qvo', data['qvo']],
                ['qvb', data['qvb']],
                ['qbr', data['qbr']],
                ['tap', data['tap']]))


class CheckDHCPonNetworkNodes(Lister):
    "Check DHCP on network nodes."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckDHCPonNetworkNodes, self).get_parser(prog_name)
        parser.add_argument('port_id', default='bad',
                            help='ID of port to look up.')
        parser.add_argument('physical_interface', default='bad',
                            help=('Name of physical interface.'
                                  'We catch packets at this interface'))
        parser.add_argument('network_type', default='vlan',
                            help='Network type, you want to check.')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        if not utils.is_uuid_like(parsed_args.port_id):
            utils.Logger.log_fail("Port id: %s is not like"
                                  "uuid." % parsed_args.port_id)
            sys.exit()
        # get network_type
        network_type = parsed_args.network_type
        if network_type != 'vlan' and network_type != 'vxlan':
            utils.Logger.log_fail("Network type %s not support!"
                                  "Please choose from 'vlan' and 'vxlan'."
                                  % network_type)
            sys.exit()
        self.log.debug("network_type is %s" % network_type)

        # get port's network_id and ip address
        port_network_id = neutron.get_port_attr(parsed_args.port_id,
                                                'network_id')
        if not port_network_id:
            utils.Logger.log_fail("Get port network_id fails."
                                  "Please check this port.")
            sys.exit()
        self.log.debug("port network id is %s" % port_network_id)

        port_ip_addr = neutron.get_port_attr(parsed_args.port_id,
                                             'fixed_ips')[0]['ip_address']
        if not port_ip_addr:
            utils.Logger.log_fail("Get port ip_addr fails."
                                  "Please check this port.")
            sys.exit()
        self.log.debug("port ip addr is %s" % port_ip_addr)

        # choose one network agent
        host_id = neutron.choose_one_network_agent(port_network_id)
        if not host_id:
            utils.Logger.log_fail("Network %s has no dhcp services."
                                  % port_network_id)
            sys.exit()
        self.log.debug("Get host %s" % host_id)

        # setup steth server
        try:
            server = utils.setup_server(host_id)
            self.log.debug("setup server: %s" % host_id)
        except:
            utils.Logger.log_fail("Setup server fail in: %s." % server)
            sys.exit()

        # get physical interface name
        physical_interface = parsed_args.physical_interface
        self.log.debug("Physical interface is %s" % physical_interface)
        res = server.check_dhcp_on_net(net_id=port_network_id,
                                       port_ip=port_ip_addr,
                                       phy_iface=physical_interface,
                                       net_type=network_type)
        self.log.debug("Response is %s" % res)
        if res['code'] == 0:
            data = res['data']
            return (['Device Name', 'Result'],
                    (['br-int', data['br-int']],
                    ['ovsbr3', data['ovsbr3']],
                    [physical_interface, data[physical_interface]]))
        return (['Error Mssage', ' '], [('message', res['message'])])
