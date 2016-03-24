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
from steth.stethclient import utils
from steth.stethclient.constants import MGMT_TYPE
from steth.stethclient.constants import NET_TYPE
from steth.stethclient.constants import STORAGE_TYPE
from steth.stethclient.utils import Logger
from steth.stethclient.utils import setup_server

try:
    from steth.stethclient.constants import MGMT_AGENTS_INFOS
    from steth.stethclient.constants import NET_AGENTS_INFOS
    from steth.stethclient.constants import STORAGE_AGENTS_INFOS
except:
    Logger.log_fail("Import configure file fail.")
    MGMT_AGENTS_INFOS = NET_AGENTS_INFOS = STORAGE_AGENTS_INFOS = {
        'agent-64': "127.0.0.1",
        'agent-65': "127.0.0.1",
    }


def get_ip_by_hostname(hostname):
    # TODO(changzhi): DNS resolve
    return socket.gethostbyname(hostname)


class CheckIperf(Lister):
    "Setup Iperf server in agent"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CheckIperf, self).get_parser(prog_name)
        parser.add_argument('server_agent', default='bad',
                            help='IPERF server will be started at this agent.')
        parser.add_argument('client_agent', default='bad',
                            help='IPERF client will be started at this agent.')
        parser.add_argument('--iperf_server_type', default='others',
                            help=("Choose from 'mgmt', 'net' or 'storage'."
                                  "If you want to all of these types, "
                                  "please choose 'others'."))
        parser.add_argument('--server_protocol', nargs='?', default='TCP')
        parser.add_argument('--server_port', nargs='?', default='5001')
        parser.add_argument('--client_protocol', nargs='?', default='TCP')
        parser.add_argument('--client_port', nargs='?', default='5001')
        parser.add_argument('--client_timeout', nargs='?', default='5')
        parser.add_argument('--client_parallel', nargs='?', default=None)
        parser.add_argument('--client_bandwidth', nargs='?', default=None)
        return parser

    def take_iperf_client(self, client, host, protocol,
                          timeout, parallel, bandwidth, port):
        res = client.start_iperf_client(protocol=protocol,
                                        host=host,
                                        timeout=timeout,
                                        parallel=parallel,
                                        bandwidth=bandwidth,
                                        port=port)
        return res

    def take_action(self, parsed_args):
        self.log.debug('Get parsed_args: %s' % parsed_args)
        server = setup_server(parsed_args.server_agent)
        client = setup_server(parsed_args.client_agent)
        iperf_server_pdid = None
        # setup iperf server
        res = server.setup_iperf_server(protocol=parsed_args.server_protocol,
                                        port=parsed_args.server_port)
        self.log.debug('Response is %s' % res)
        if res['code'] != 0:
            Logger.log_fail(res['message'])
            sys.exit()
        if res['code'] == 0:
            msg = (('Iperf server setup success and runs in '
                    'pid:%s') % (res['data']['pid']))
            self.log.debug(msg)
            iperf_server_pdid = res['data']['pid']
        if parsed_args.iperf_server_type == MGMT_TYPE or \
           parsed_args.iperf_server_type == NET_TYPE or \
           parsed_args.iperf_server_type == STORAGE_TYPE:
            host = utils.get_ip_from_agent(parsed_args.server_agent,
                                           parsed_args.iperf_server_type)
            bandwidth = parsed_args.client_bandwidth
            # setup iperf client
            res = self.take_iperf_client(client=client,
                                         protocol=parsed_args.client_protocol,
                                         host=host,
                                         timeout=parsed_args.client_timeout,
                                         parallel=parsed_args.client_parallel,
                                         bandwidth=bandwidth,
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
        elif parsed_args.iperf_server_type == 'others':
            mgmt_host = MGMT_AGENTS_INFOS[parsed_args.server_agent]
            net_host = NET_AGENTS_INFOS[parsed_args.server_agent]
            storage_host = STORAGE_AGENTS_INFOS[parsed_args.server_agent]
            bandwidth = parsed_args.client_bandwidth
            mgmt_res = self.take_iperf_client(
                client=client,
                protocol=parsed_args.client_protocol,
                host=mgmt_host,
                timeout=parsed_args.client_timeout,
                parallel=parsed_args.client_parallel,
                bandwidth=bandwidth,
                port=parsed_args.client_port)
            msg = ("Start iperf client from MGMT network success. "
                   "Begain network iperf...")
            Logger.log_normal(msg)
            net_res = self.take_iperf_client(
                client=client,
                protocol=parsed_args.client_protocol,
                host=net_host,
                timeout=parsed_args.client_timeout,
                parallel=parsed_args.client_parallel,
                bandwidth=bandwidth,
                port=parsed_args.client_port)
            msg = ("Start iperf client from NET network success. "
                   "Begain storage iperf...")
            Logger.log_normal(msg)
            storage_res = self.take_iperf_client(
                client=client,
                protocol=parsed_args.client_protocol,
                host=storage_host,
                timeout=parsed_args.client_timeout,
                parallel=parsed_args.client_parallel,
                bandwidth=bandwidth,
                port=parsed_args.client_port)
            # kill iperf server
            r = server.teardown_iperf_server(iperf_server_pdid)
            if r['code'] == 1:
                Logger.log_fail(r['message'])
            if r['code'] == 0:
                msg = (('Iperf server delete success and '
                        'pid:%s') % (iperf_server_pdid))
                self.log.debug(msg)
            if mgmt_res['code'] == 0 and \
               net_res['code'] == 0 and \
               storage_res['code'] == 0:
                mgmt_data = [(k, v) for k, v in mgmt_res['data'].items()]
                net_data = [(k, v) for k, v in net_res['data'].items()]
                storage_data = [(k, v) for k, v in storage_res['data'].items()]
                return (('Field', 'Value'),
                        [('Mgmt Result', ' ')] +
                        mgmt_data +
                        [('Net Result', ' ')] +
                        net_data +
                        [('Storage Result', ' ')] +
                        storage_data)
            msg = ("One of start iperf clients error. Please check.")
            return (['Error Mssage', ' '], [('message', msg)])
        else:
            msg = ("Get unsupport iperf server type: %s. "
                   "Please choose from 'net', 'mgmt', 'storage', 'others'. "
                   % parsed_args.iperf_server_type)
            Logger.log_fail(msg)
            sys.exit()
