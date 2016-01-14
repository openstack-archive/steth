# Copyright 2016 UnitedStack, Inc.
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

import uuid
from stetho.agent.common import log
from stetho.agent.common import utils

LOG = log.get_logger()

OUT_DIR = '/tmp/'


class IPerfDriver(object):

    def start_server(self, protocol='TCP', port=5001, mss=None, window=None):
        """iperf -s -D --mss mss
        """
        id = uuid.uuid4()
        output = OUT_DIR + 'iperf-server-%s' % id
        utils.replace_file(output)
        cmd = ['iperf', '-s', '-D', '-p', str(port), '-o', output]
        if not cmp(protocol, 'UDP'):
            cmd.append('-u')
        if mss:
            cmd.extend(['-m', str(mss)])
        if window:
            cmd.extend(['-w', str(window)])
        cmd.extend(['>', output])
        pid = utils.create_deamon(cmd)
        data = dict()
        data['id'] = id
        data['pid'] = pid
        return data

    def stop_server(self, pid):
        utils.kill_process_by_id(pid)

    def start_client(self, host, port=5001, protocol='TCP', time=60,
                     parallel=None, bandwidth=None):
        """iperf -D -c host -t 60
        """
        id = uuid.uuid4()
        output = OUT_DIR + 'iperf-client-%s' % id
        utils.replace_file(output)
        cmd = ['iperf', '-D', '-c', host, '-p', str(port), '-t', str(time)]
        if not (protocol, 'UDP'):
            cmd.append('-u')
        if parallel:
            cmd.extend(['-P', str(parallel)])
        if bandwidth:
            cmd.extend(['-b', '%sM' % bandwidth])
        cmd.extend(['>', output])
        utils.create_deamon(cmd)
        data = dict()
        data['id'] = id
        return data

    def get_server_output(self, id):
        # TODO: some analysis
        pass

    def get_client_output(self, id):
        # TODO: some analysis
        pass
