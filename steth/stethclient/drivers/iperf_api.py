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
import socket
import sys

from cliff.lister import Lister
from steth.stethclient.utils import Logger
from steth.stethclient.utils import setup_server
from steth.stethclient import utils


def get_ip_by_hostname(hostname):
    # TODO(changzhi): DNS resolve
    return socket.gethostbyname(hostname)


class CheckIperf(Lister):
    "Setup Iperf server in agent"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckIperf, self).get_parser(prog_name)
        parser.add_argument('server_agent', default='bad')
        parser.add_argument('client_agent', default='bad')
        parser.add_argument('iperf_server_ip', default='bad')
        parser.add_argument('--server_protocol', nargs='?', default='TCP')
        parser.add_argument('--server_port', nargs='?', default='5001')
        parser.add_argument('--client_protocol', nargs='?', default='TCP')
        parser.add_argument('--client_port', nargs='?', default='5001')
        parser.add_argument('--client_timeout', nargs='?', default='5')
        parser.add_argument('--client_parallel', nargs='?', default=None)
        parser.add_argument('--client_bandwidth', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        # check iperf client ip if legal
        if utils.is_ip(parsed_args.iperf_server_ip):
            Logger.log_fail('IP address not legal')
            sys.exit()
        server = setup_server(parsed_args.server_agent)
        client = setup_server(parsed_args.client_agent)
        iperf_server_pdid = None
        # check iperf client ip exist
        res = server.validate_ip(parsed_args.iperf_server_ip)
        if res['code'] == 1:
            Logger.log_fail(res['message'])
            sys.exit()
        # setup iperf server
        res = server.setup_iperf_server(protocol=parsed_args.server_protocol,
                                        port=parsed_args.server_port)
        self.log.debug('Response is %s' % res)
        if res['code'] == 1:
            Logger.log_fail(res['message'])
            sys.exit()
        if res['code'] == 0:
            msg = (('Iperf server setup success and runs in '
                    'pid:%s') % (res['data']['pid']))
            self.log.debug(msg)
            iperf_server_pdid = res['data']['pid']
        # setup iperf client
        #try:
        #    host = get_ip_by_hostname(parsed_args.server_agent)
        #except Exception as e:
        #    self.log.info("We can not resolve this name: %s",
        #        (parsed_args.server_agent))
        res = client.start_iperf_client(protocol=parsed_args.client_protocol,
                                        host=parsed_args.iperf_server_ip,
                                        timeout=parsed_args.client_timeout,
                                        parallel=parsed_args.client_parallel,
                                        bandwidth=parsed_args.client_bandwidth,
                                        port=parsed_args.client_port)
        self.log.debug('Response is %s' % res)
        # kill iperf server
        r = server.teardown_iperf_server(iperf_server_pdid)
        if r['code'] == 1:
            Logger.log_fail(r['message'])
        if r['code'] == 0:
            msg = (('Iperf server delete success and '
                    'pid:%s') % (iperf_server_pdid))
            self.log.debug(msg)
        return (('Field', 'Value'),
                ((k, v) for k, v in res['data'].items()))
