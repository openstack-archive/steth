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
from steth.agent import api
from steth.agent.common import utils as agent_utils


class TestApi(unittest.TestCase):
    def setUp(self):
        self.agent_api = api.AgentApi()

    @mock.patch('steth.agent.common.utils.execute')
    def test_check_ports_on_br(self, execute):
        execute.return_value = (0, [''])
        result = self.agent_api.check_ports_on_br('br-ex', 'eth3')
        self.assertEqual(execute.called, True)
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.common.utils.execute')
    def test_ping(self, execute):
        stdout = ['', '2 packets transmitted, 2 received, 0% packet loss', '']
        execute.return_value = (0, stdout)
        result = self.agent_api.ping(['1.2.4.8', '1.2.4.9'])
        self.assertEqual(result['code'], 0)

    def test_get_interface(self):
        get_interface = mock.Mock(return_value=(0, '', dict()))
        agent_utils.get_interface = get_interface
        self.agent_api.get_interface()
        self.assertEqual(agent_utils.get_interface.called, True)

    @mock.patch('steth.agent.common.utils.execute')
    def test_set_link(self, execute):
        stdout = ['', '']
        execute.return_value = (0, stdout)
        result = self.agent_api.setup_link('eth0', '10.0.0.100/24')
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.common.utils.execute')
    def test_teardown_link(self, execute):
        stdout = ['', '']
        execute.return_value = (0, stdout)
        result = self.agent_api.teardown_link('eth0')
        self.assertEqual(result['code'], 0)
        execute.return_value = (1, stdout)
        result = self.agent_api.teardown_link('eth0')
        self.assertEqual(result['code'], 1)

    @mock.patch('steth.agent.common.utils.create_deamon')
    def test_start_iperf_server(self, create_deamon):
        create_deamon.return_value = 100
        result = self.agent_api.setup_iperf_server('UDP')
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.common.utils.kill_process_by_id')
    def test_teardown_iperf_server(self, kill_process_by_id):
        result = self.agent_api.setup_iperf_server(100)
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.common.utils.execute_wait')
    def test_start_iperf_client(self, execute_wait):
        stdout = '[  3]  0.0- 3.0 sec   497 MBytes  1.39 Gbits/sec'
        execute_wait.return_value = (0, stdout, '')
        result = self.agent_api.start_iperf_client(host='127.0.0.1')
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.common.utils.execute')
    def test_validate_ip(self, execute):
        stdout = ['', '']
        execute.return_value = (0, stdout)
        result = self.agent_api.validate_ip('1.2.3.4')
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.drivers.pcap_driver.PcapDriver')
    @mock.patch('steth.agent.drivers.scapy_driver.ScapyDriver')
    def test_check_dhcp_on_comp(self, PcapDriver, ScapyDriver):
        port_id = '27a9a962-8049-48c3-b77f-0653f8ee34df'
        port_mac = 'fa:16:3e:18:fd:f7'
        phy_iface = 'eth3'
        net_type = 'vlan'
        result = self.agent_api.check_dhcp_on_comp(port_id, port_mac,
                                                   phy_iface, net_type)
        self.assertEqual(result['code'], 0)

    @mock.patch('steth.agent.drivers.pcap_driver.PcapDriver')
    @mock.patch('steth.agent.drivers.scapy_driver.ScapyDriver')
    def test_check_dhcp_on_comp_vxlan(self, PcapDriver, ScapyDriver):
        port_id = '27a9a962-8049-48c3-b77f-0653f8ee34df'
        port_mac = 'fa:16:3e:18:fd:f7'
        phy_iface = 'eth3'
        net_type = 'vxlan'
        self.agent_api.check_dhcp_on_comp(port_id, port_mac,
                                          phy_iface, net_type)
        self.assertRaises(Exception())

    def test_say_hello(self):
        self.agent_api.say_hello()
        self.assertEqual(agent_utils.make_response.called, True)
