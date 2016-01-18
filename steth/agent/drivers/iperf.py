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

from steth.agent.common import log
from steth.agent.common import utils

LOG = log.get_logger()

OUT_DIR = '/tmp/'


class IPerfDriver(object):

    def start_server(self, protocol='TCP', port=5001, mss=None, window=None):
        """iperf -s -D --mss mss
        """
        cmd = ['iperf', '-s', '-p', str(port)]
        if not cmp(protocol, 'UDP'):
            cmd.append('-u')
        if mss:
            cmd.extend(['-M', str(mss)])
        if window:
            cmd.extend(['-w', str(window)])
        pid = utils.create_deamon(cmd)
        data = dict()
        data['pid'] = pid
        return data

    def stop_server(self, pid):
        utils.kill_process_by_id(pid)

    def start_client(self, host, port=5001, protocol='TCP', timeout=5,
                     parallel=None, bandwidth=None):
        """iperf -D -c host -t 60
        """
        cmd = ['iperf', '-c', host, '-p', str(port), '-t', str(timeout)]
        if not (protocol, 'UDP'):
            cmd.append('-u')
        if parallel:
            cmd.extend(['-P', str(parallel)])
        if bandwidth:
            cmd.extend(['-b', '%sM' % bandwidth])
        stdcode, stdout, stderr = utils.execute_wait(cmd)
        if (not stdcode) or (not stderr):
            out_dict = stdout.split('\n')
            if not out_dict[-1]:
                out_dict.pop()
            out_data = out_dict[-1].split()
            data = dict()
            data['Bandwidth'] = out_data[-2] + ' ' + out_data[-1]
            data['Transfer'] = out_data[-4] + ' ' + out_data[-3]
            data['Interval'] = out_data[-6]
            return data
        raise Exception('Start iperf failed, please check on the node.')
