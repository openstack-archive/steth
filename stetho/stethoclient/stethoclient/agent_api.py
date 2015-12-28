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
from stethoclient.constants import AGENT_INFOS

LISTEN_PORT = 9698


class PingAgent(Command):
    "Get agent status."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('sending message!')
        self.log.debug('sending debug message!')
        self.app.stdout.write('hi!')


class GetInterface(Lister):
    "A test function that show a message"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetInterface, self).get_parser(prog_name)
        parser.add_argument('agent', default='bad')
        parser.add_argument('interface', default='eth0')
        return parser

    def setup_server(self, parsed_args):
        if parsed_args.agent in AGENT_INFOS:
            self.log.debug('get agent:%s ip_address:%s' % (
                parsed_args.agent, AGENT_INFOS[parsed_args.agent]))
        else:
            self.log.error('Agent %s not configured. Please check it.' % (
                            parsed_args.agent))
            sys.exit()
        self.log.debug('Begin create connection with http://%s:9698.' % (
                        parsed_args.agent))
        server = jsonrpclib.Server('http://%s:%s' % (
                 AGENT_INFOS[parsed_args.agent], LISTEN_PORT))
        self.log.debug('Create connection with %s success.' % (
                        parsed_args.agent))
        return server

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        self.log.debug('Agent is %s' % parsed_args.agent)
        self.log.debug('Interface is %s' % parsed_args.interface)
        server = self.setup_server(parsed_args)
        try:
            res = server.get_interface(parsed_args.interface)
            self.log.debug('Response is %s' % res)
            if res['code'] == 0:
                return (('Field', 'Value'),
                        ((k, v) for k, v in res['data'].items()))
        except:
            self.log.error('Agent %s return error!' % parsed_args.agent)
            sys.exit()
