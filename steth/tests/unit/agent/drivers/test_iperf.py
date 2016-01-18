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

import mock
import unittest
from steth.agent.drivers import iperf
from steth.agent.common import utils


class TestIPerfDriver(unittest.TestCase):
    def setUp(self):
        self.iperfd = iperf.IPerfDriver()

    def test_start_server(self):
        utils.create_deamon = mock.Mock(return_value=1000)
        data = self.iperfd.start_server(protocol='UDP')
        self.assertEqual(data['pid'], 1000)

    def test_start_client(self):
        stdout = '[  3]  0.0- 3.0 sec   497 MBytes  1.39 Gbits/sec'
        utils.execute_wait = mock.Mock(return_value=(0, stdout, ''))
        self.iperfd.start_client('127.0.0.1')
        self.assertEqual(utils.execute_wait.called, True)
