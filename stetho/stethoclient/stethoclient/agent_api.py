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
import jsonrpclib
import sys

from cliff.command import Command
from cliff.lister import Lister
from json import JSONDecoder
from stetho.stethoclient.constants import AGENT_INFOS

LISTEN_PORT = 9698


def setup_server(agent):
    log = logging.getLogger(__name__)
    if agent in AGENT_INFOS:
        log.debug('get agent:%s ip_address:%s' % (
            agent, AGENT_INFOS[agent]))
    else:
        log.error('Agent %s not configured. Please check it.' % (
                         agent))
        sys.exit()
    log.debug('Begin create connection with http://%s:9698.' % (
                    agent))
    server = jsonrpclib.Server('http://%s:%s' % (
             AGENT_INFOS[agent], LISTEN_PORT))
    log.debug('Create connection with %s success.' % (agent))
    return server


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
            self.log.error('Error %s has occured.' % res)


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
        try:
            # Setup Link
            server.setup_link(parsed_args.interface,
                              parsed_args.cidr)
            # Get Link info
            res = server.get_interface(parsed_args.interface)
            self.log.debug('Response is %s' % res)
            if res['code'] == 0:
                return (('Field', 'Value'),
                        ((k, v) for k, v in res['data'].items()))
        except Exception as e:
            self.log.error('Agent %s return error: %s!' % parsed_args.agent, e)
            sys.exit()


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
        try:
            res = server.get_interface(parsed_args.interface)
            self.log.debug('Response is %s' % res)
            if res['code'] == 0:
                return (('Field', 'Value'),
                        ((k, v) for k, v in res['data'].items()))
        except:
            self.log.error('Agent %s return error!' % parsed_args.agent)
            sys.exit()


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
        try:
            dest = parsed_args.destination.split(',')
            res = server.ping(ips=dest,
                              count=parsed_args.count,
                              timeout=parsed_args.timeout,
                              interface=parsed_args.interface)
            self.log.debug('Response is %s' % res)
            if res['code'] == 0:
                return (('Destination', 'Packet Loss (%)'),
                        ((k, v) for k, v in res['data'].items()))
        except Exception as e:
            self.log.error('Agent %s return error: %s!' % parsed_args.agent, e)
            sys.exit()


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
            if res['code'] == 0:
                return (('Port', 'Exists'),
                        ((k, v) for k, v in res['data'].items()))
        except Exception as e:
            self.log.error('Agent %s return error: %s!' % parsed_args.agent, e)
            sys.exit()
