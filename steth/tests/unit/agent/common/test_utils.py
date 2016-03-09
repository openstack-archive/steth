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

import os
import mock
import unittest
import types
import platform
from steth.agent.common import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_file = self.get_temp_file_path('test_execute.tmp')
        open(self.test_file, 'w+').close()
        self.pids = list()

    def test_execute(self):
        expected = "%s\n" % self.test_file
        code, result = utils.execute(["ls", self.test_file])
        self.assertEqual(0, code)
        self.assertEqual(result.pop(), expected.strip('\n'))

    def get_temp_file_path(self, filename, root=None):
        root = '/tmp/%s'
        return root % filename

    def test_make_response(self):
        para = dict()
        para['code'] = 0
        para['message'] = 'Test make response.'
        para['data'] = dict()
        result = utils.make_response(para['code'], para['message'],
                                     para['data'])
        self.assertEqual(para, result)

    @mock.patch('steth.agent.common.utils.execute')
    def test_get_interface(self, execute):
        # test centos 6.5
        platform.linux_distribution = mock.Mock(return_value=['', '6.5', ''])
        out = ['eth0      Link encap:Ethernet  HWaddr FA:16:3E:61:F2:CF',
               'inet addr:10.0.1.104  Bcast:10.0.1.255  Mask:255.255.255.0',
               'inet6 addr: fe80::f816:3eff:fe61:f2cf/64 Scope:Link',
               'UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1',
               'RX packets:20121 errors:0 dropped:0 overruns:0 frame:0',
               'TX packets:10163 errors:0 dropped:0 overruns:0 carrier:0',
               'collisions:0 txqueuelen:1000',
               'RX bytes:19492218 (18.5 MiB)  TX bytes:1173768 (1.1 MiB)']
        execute.return_value = (0, out)
        self.assertEqual(utils.get_interface('eth0')[0], 0)
        # test centos 7.0
        platform.linux_distribution = mock.Mock(return_value=['', '7.0', ''])
        out = ['eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500',
               'inet 10.0.1.101  netmask 255.255.255.0  broadcast 10.0.1.255',
               'inet6 fe80::f816:3eff:fe6f:1a9d  prefixlen 64  scopeid 0x20<l',
               'ether fa:16:3e:6f:1a:9d  txqueuelen 1000  (Ethernet)',
               'RX packets 415365  bytes 150440678 (143.4 MiB)',
               'RX errors 0  dropped 0  overruns 0  frame 0',
               'TX packets 275332  bytes 91891644 (87.6 MiB)',
               'TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0']
        execute.return_value = (0, out)
        self.assertEqual(utils.get_interface('eth0')[0], 0)
        # test centos 8.1
        platform.linux_distribution = mock.Mock(return_value=['', '7.1', ''])
        self.assertEqual(utils.get_interface('eth0')[0], 0)
        # test other distribution
        platform.linux_distribution = mock.Mock(return_value=['', '6.6', ''])
        self.assertEqual(utils.get_interface('eth0')[0], 1)

    def test_create_deamon(self):
        cmd = ["ls", self.test_file]
        pid = utils.create_deamon(cmd)
        self.pids.append(pid)
        self.assertEqual(type(pid), types.IntType)

    def test_kill_process_by_id(self):
        pid = 100
        os.kill = mock.Mock()
        os.waitpid = mock.Mock()
        utils.kill_process_by_id(pid)
        self.assertEqual(os.kill.called, True)
