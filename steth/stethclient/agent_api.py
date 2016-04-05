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
from steth.stethclient import utils
from steth.stethclient.utils import Logger
from steth.stethclient.utils import setup_server

SETUP_LINK_IP_PRE = "192.168.100."
ACTIVE = ':-)'
DOWN = 'XXX'


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
        res = server.teardown_link(parsed_args.interface)
        if not res['code']:
            Logger.log_normal("Delete interface success.")
        else:
            Logger.log_fail(res['message'])


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
    "Get interface detail information."

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
        for ip in dest:
            if utils.is_ip(ip):
                Logger.log_fail("%s is invalid." % ip)
                sys.exit()
        Logger.log_normal("Ping start...")
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
        res = server.check_ports_on_br(parsed_args.bridge,
                                       [parsed_args.port])
        self.log.debug('Response is %s' % res)
        if res['code']:
            Logger.log_fail(res['message'])
            sys.exit()
        return (('Port', 'Is Exist'),
                ((k, v) for k, v in res['data'].items()))


class CheckVlanInterface(Command):
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
        # First of all, check the interface existence
        serverA_interface_existence = serverA.get_interface(interface)
        serverB_interface_existence = serverB.get_interface(interface)

        if serverA_interface_existence['code'] == 1:
            msg = ("Agent: %s has no interface named %s!"
                   "This interface will be created." % (parsed_args.agentA,
                                                        interface))
            Logger.log_fail(msg)
            resA = serverA.add_vlan_to_interface(parsed_args.interface,
                                                 parsed_args.vlan_id)
            self.log.debug('Create interface success for %s' % resA)
        if serverB_interface_existence['code'] == 1:
            msg = ("Agent: %s has no interface named %s!"
                   "This interface will be created." % (parsed_args.agentB,
                                                        interface))
            Logger.log_fail(msg)
            resB = serverB.add_vlan_to_interface(parsed_args.interface,
                                                 parsed_args.vlan_id)
            self.log.debug('Create interface success for %s' % resB)
        # setup link in each agent
        ipA = SETUP_LINK_IP_PRE + parsed_args.agentA.split('-')[1] + '/24'
        resA = serverA.setup_link(interface, ipA)
        self.log.debug('Response is %s' % resA)
        ipB = SETUP_LINK_IP_PRE + parsed_args.agentB.split('-')[1] + '/24'
        resB = serverB.setup_link(interface, ipB)
        self.log.debug('Response is %s' % resB)
        # ping a agent from exists IP to check connectivity
        res = serverA.ping(ips=[ipB])
        # teardown the interface if steth created it.
        if serverA_interface_existence['code']:
            resA = serverA.teardown_link(interface)
        if serverB_interface_existence['code']:
            resB = serverB.teardown_link(interface)
        if res['code'] == 0:
            Logger.log_normal("Packet loss is %s%%" % res['data'].values()[0])
            sys.exit()
        msg = "Error happens because %s" % res['message']
        Logger.log_fail(msg)


class PrintAgentsInfo(Lister):
    """Print all agents info."""

    def get_parser(self, prog_name):
        parser = super(PrintAgentsInfo, self).get_parser(prog_name)
        return parser

    def is_agent_active(self, agent):
        server = setup_server(agent)
        try:
            server.say_hello()
            return 0
        except:
            # If this agent is down, "Connection refused" will happen.
            return 1

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
            agent_status = ACTIVE if not self.is_agent_active(agent) else DOWN
            r.append(agent_status)
            results.append(r)
        return (('Agent Name', 'Management IP', 'Network IP', 'Storage IP',
                'Alive'), results)
