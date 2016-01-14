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

import mock
import unittest
from stetho.agent import api
from stetho.agent.common import utils as agent_utils


class TestApi(unittest.TestCase):
    def setUp(self):
        self.agent_api = api.AgentApi()

    def test_check_ports_on_br(self):
        agent_utils.execute = mock.Mock(return_value=(0, ['execute']))
        agent_utils.make_response = mock.Mock(return_value=dict())
        self.agent_api.check_ports_on_br()
        self.assertEqual(agent_utils.execute.called, True)
        self.assertEqual(agent_utils.make_response.called, True)
        agent_utils.execute = mock.Mock(return_value=(1, ['execute']))
        self.agent_api.check_ports_on_br()
        self.assertEqual(agent_utils.make_response.called, True)

    def test_ping(self):
        stdout = ['', '2 packets transmitted, 2 received, 0% packet loss', '']
        agent_utils.execute = mock.Mock(return_value=(0, stdout))
        agent_utils.make_response = mock.Mock(return_value=dict())
        self.agent_api.ping(['1.2.4.8', '1.2.4.9'])
        self.assertEqual(agent_utils.make_response.called, True)
        stdout = 'stdout'
        agent_utils.execute = mock.Mock(return_value=(0, stdout))
        self.agent_api.ping(['1.2.4.8', '1.2.4.9'])
        self.assertEqual(agent_utils.make_response.called, True)

    def test_get_interface(self):
        get_interface = mock.Mock(return_value=(0, '', dict()))
        agent_utils.get_interface = get_interface
        self.agent_api.get_interface()
        self.assertEqual(agent_utils.get_interface.called, True)

    def test_set_link(self):
        stdout = ['', '']
        agent_utils.execute = mock.Mock(return_value=(0, stdout))
        self.agent_api.setup_link('eth0', '10.0.0.100/24')
        self.assertEqual(agent_utils.make_response.called, True)
        agent_utils.execute = mock.Mock(return_value=(1, stdout))
        self.agent_api.setup_link('eth0', '10.0.0.100/24')
        self.assertEqual(agent_utils.make_response.called, True)

    def test_teardown_link(self):
        stdout = ['', '']
        agent_utils.execute = mock.Mock(return_value=(0, stdout))
        self.agent_api.teardown_link('eth0')
        self.assertEqual(agent_utils.make_response.called, True)
        agent_utils.execute = mock.Mock(return_value=(1, stdout))
        self.agent_api.teardown_link('eth0')
        self.assertEqual(agent_utils.make_response.called, True)
