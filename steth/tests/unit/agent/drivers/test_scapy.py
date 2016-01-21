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
from scapy import all as scapy
from steth.agent.drivers import scapy_driver
from steth.agent.common import constants


class TestScapyDriver(unittest.TestCase):
    def setUp(self):
        self.scapy_dri = scapy_driver.ScapyDriver()

    @mock.patch('scapy.all.sendp')
    def test_send_dhcp_over_qvb(self, sendp):
        port_id = '27a9a962-8049-48c3-b77f-0653f8ee34df'
        port_mac = 'fa:16:3e:18:fd:f7'
        self.scapy_dri.send_dhcp_over_qvb(port_id, port_mac)
        self.assertTrue(sendp.called, True)

    def test_get_dhcp_mt(self):
        dhcp = scapy.DHCP(options=[("message-type", "discover"), "end"])
        pkt = scapy.Ether() / scapy.IP() / scapy.UDP() / scapy.BOOTP() / dhcp
        message = self.scapy_dri.get_dhcp_mt(str(pkt))
        self.assertIn(message, constants.DHCP_MESSATE_TYPE)
