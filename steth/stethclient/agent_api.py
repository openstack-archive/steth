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

from cliff.command import Command
from cliff.lister import Lister
from steth.stethclient.utils import Logger
from steth.stethclient.utils import setup_server

SETUP_LINK_IP_PRE = "192.168.100."


class TearDownLink(Command):
    "Delete a link"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TearDownLink, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('interface', default='.')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        self.log.debug('Agent is %s' % parsed_args.agent)
        self.log.debug('Interface is %s' % parsed_args.interface)
        server = setup_server(parsed_args.agent)
        try:
            res = server.teardown_link(parsed_args.interface)
        except Exception as e:
            self.log.error('Error %s has occured because: %s' % (res, e))


class SetUpLink(Lister):
    "Setup a link"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SetUpLink, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('interface', default='eth0')
        parser.add_argument('cidr', default='.')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        self.log.debug('Agent is %s' % parsed_args.agent)
        self.log.debug('Interface is %s' % parsed_args.interface)
        self.log.debug('Cidr is %s' % parsed_args.cidr)
        server = setup_server(parsed_args.agent)
        # Setup Link
        server.setup_link(parsed_args.interface,
                          parsed_args.cidr)
        # Get Link info
        res = server.get_interface(parsed_args.interface)
        self.log.debug('Response is %s' % res)
        if res['code'] == 1:
            Logger.log_fail(res['message'])
            sys.exit()
        if res['code'] == 0:
            return (('Field', 'Value'),
                    ((k, v) for k, v in res['data'].items()))
        return (['Error Mssage', ' '], [('message', res['message'])])


class GetInterface(Lister):
    "A test function that show a message"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetInterface, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('interface', default='eth0')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        self.log.debug('Agent is %s' % parsed_args.agent)
        self.log.debug('Interface is %s' % parsed_args.interface)
        server = setup_server(parsed_args.agent)
        res = server.get_interface(parsed_args.interface)
        self.log.debug('Response is %s' % res)
        if res['code'] == 0:
            return (('Field', 'Value'),
                    ((k, v) for k, v in res['data'].items()))
        return (['Error Mssage', ' '], [('message', res['message'])])


class AddVlanToInterface(Lister):
    "Setup a link"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AddVlanToInterface, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('interface', default='eth0')
        parser.add_argument('vlan_id', default='1124')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        self.log.debug('Agent is %s' % parsed_args.agent)
        self.log.debug('Interface is %s' % parsed_args.interface)
        self.log.debug('Vlan_id is %s' % parsed_args.vlan_id)
        server = setup_server(parsed_args.agent)
        try:
            # Setup Link
            server.add_vlan_to_interface(parsed_args.interface,
                                         parsed_args.vlan_id)
            # Get Link info
            new_interface = parsed_args.interface + '.' + parsed_args.vlan_id
            res = server.get_interface(new_interface)
            self.log.debug('Response is %s' % res)
            if res['code'] == 1:
                Logger.log_fail(res['message'])
                sys.exit()
            if res['code'] == 0:
                return (('Field', 'Value'),
                        ((k, v) for k, v in res['data'].items()))
        except Exception as e:
            self.log.error('Agent %s return error: %s!' % parsed_args.agent, e)
            sys.exit()


class AgentPing(Lister):
    "Ping a destination from one agent"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(AgentPing, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('destination', default='1.2.4.8')
        parser.add_argument('--count', nargs='?', default='2')
        parser.add_argument('--timeout', nargs='?', default='2')
        parser.add_argument('--interface', nargs='?', default='eth0')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        server = setup_server(parsed_args.agent)
        dest = parsed_args.destination.split(',')
        res = server.ping(ips=dest,
                          count=parsed_args.count,
                          timeout=parsed_args.timeout,
                          interface=parsed_args.interface)
        self.log.debug('Response is %s' % res)
        if res['code'] == 1:
            Logger.log_fail(res['message'])
            sys.exit()
        if res['code'] == 0:
            return (('Destination', 'Packet Loss (%)'),
                    ((k, v) for k, v in res['data'].items()))
        return (['Error Mssage', ' '], [('message', res['message'])])


class CheckPortsOnBr(Lister):
    "Check a port if exists on a ovs bridge"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckPortsOnBr, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('bridge', default='br-int')
        parser.add_argument('port', default='br-int')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        server = setup_server(parsed_args.agent)
        try:
            res = server.check_ports_on_br(parsed_args.bridge,
                                           parsed_args.port)
            self.log.debug('Response is %s' % res)
            if res['code'] == 1:
                Logger.log_fail(res['message'])
                sys.exit()
            if res['code'] == 0:
                return (('Port', 'Exists'),
                        ((k, v) for k, v in res['data'].items()))
        except Exception as e:
            self.log.error('Agent %s return error: %s!' % parsed_args.agent, e)
            sys.exit()


class CheckVlanInterface(Lister):
    """Check vlan if exists in switch"""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckVlanInterface, self).get_parser(prog_name)
        parser.add_argument('agentA', default='bad')
        parser.add_argument('agentB', default='bad')
        parser.add_argument('interface', default='eth0')
        parser.add_argument('vlan_id', default='1124')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        serverA = setup_server(parsed_args.agentA)
        serverB = setup_server(parsed_args.agentB)
        interface = parsed_args.interface + '.' + parsed_args.vlan_id
        # First of all, check the interface if exists
        resA = serverA.get_interface(interface)
        resB = serverB.get_interface(interface)
        if resA['code'] == 1:
            msg = "Agent: %s has no interface named %s!" % (
                parsed_args.agentA, interface)
            Logger.log_fail(msg)
            sys.exit()
        if resB['code'] == 1:
            msg = "Agent: %s has no interface named %s!" % (
                parsed_args.agentB, interface)
            Logger.log_fail(msg)
            sys.exit()
        # add vlan interface in each agent
        resA = serverA.add_vlan_to_interface(parsed_args.interface,
                                             parsed_args.vlan_id)
        self.log.debug('Response is %s' % resA)
        resB = serverB.add_vlan_to_interface(parsed_args.interface,
                                             parsed_args.vlan_id)
        self.log.debug('Response is %s' % resB)
        Logger.log_normal(('AgentA and agentB has already added the '
                           'interface %s ') % (interface))
        # setup link in each agent
        ipA = SETUP_LINK_IP_PRE + parsed_args.agentA.split('-')[1] + '/24'
        resA = serverA.setup_link(interface, ipA)
        self.log.debug('Response is %s' % resA)
        ipB = SETUP_LINK_IP_PRE + parsed_args.agentB.split('-')[1] + '/24'
        resB = serverB.setup_link(interface, ipB)
        self.log.debug('Response is %s' % resB)
        Logger.log_normal(('AgentA and agentB has already setup the '
                           'IP %s and IP %s') % (ipA, ipB))
        # ping a agent from exists IP to check connectivity
        res = serverA.ping(ips=[ipB])
        # teardown the interface in each agent to clean all resources
        resA = serverA.teardown_link(interface)
        self.log.debug('Response is %s' % resA)
        resB = serverB.teardown_link(interface)
        self.log.debug('Response is %s' % resB)
        Logger.log_normal(('AgentA and agentB has already deleted the'
                           'vlan %s in %s') % (parsed_args.vlan_id,
                                               parsed_args.interface))
        if res['code'] == 0:
            return (('Destination', 'Packet Loss (%)'),
                    ((k, v) for k, v in res['data'].items()))
        return (['Error Mssage', ' '], [('message', res['message'])])


class PrintAgentsInfo(Lister):
    """Print all agents info."""

    def get_parser(self, prog_name):
        parser = super(PrintAgentsInfo, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        try:
            from steth.stethclient.constants import MGMT_AGENTS_INFOS
            from steth.stethclient.constants import NET_AGENTS_INFOS
            from steth.stethclient.constants import STORAGE_AGENTS_INFOS
        except Exception as e:
            Logger.log_fail("Import configure file fail. Because: %s!" % e)
            sys.exit()

        results = []
        for agent in MGMT_AGENTS_INFOS.keys():
            r = []
            r.append(agent)
            r.append(MGMT_AGENTS_INFOS[agent])
            r.append(NET_AGENTS_INFOS[agent])
            r.append(STORAGE_AGENTS_INFOS[agent])
            results.append(r)
        return (('Agent Name', 'Management IP', 'Network IP', 'Storage IP'),
                results)
