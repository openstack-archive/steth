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
from steth.agent.drivers import pcap_driver
from steth.agent.common import utils
from steth.agent.common import constants


class TestPcapDriver(unittest.TestCase):
    def setUp(self):
        """Get interfaces on host for check.
        """
        self.iface = 'eth0'
        self.filter = '(tcp and port 80)'
        self.pcap_dri = pcap_driver.PcapDriver()

    @mock.patch('pcap.pcap')
    def test_setup_listener(self, pcap):
        self.pcap_dri.setup_listener(self.iface, self.filter)
        pcap.assert_called_with(self.iface, timeout_ms=2000)
        pcap(self.iface).setfilter.assert_called_with(self.filter)

    @mock.patch('steth.agent.drivers.pcap_driver.PcapDriver.setup_listener')
    def test_setup_listener_on_comp(self, setup_listener):
        port_id = '27a9a962-8049-48c3-b77f-0653f8ee34df'
        listeners = self.pcap_dri.setup_listener_on_comp(port_id, self.filter)
        tap_device = utils.get_vif_name(constants.TAP_DEVICE_PREFIX, port_id)
        qvb_device = utils.get_vif_name(constants.QVB_DEVICE_PREFIX, port_id)
        qbr_device = utils.get_vif_name(constants.QBR_DEVICE_PREFIX, port_id)
        qvo_device = utils.get_vif_name(constants.QVO_DEVICE_PREFIX, port_id)
        vif_devices = [tap_device, qvb_device, qbr_device, qvo_device]
        map(lambda vif: setup_listener.assert_any_call(vif, self.filter),
            vif_devices)
        self.assertEqual(len(listeners), 4)

    @mock.patch('pcap.pcap')
    def test_set_nonblock(self, pcap):
        listener = self.pcap_dri.setup_listener(self.iface, self.filter)
        self.pcap_dri.set_nonblock(listener)
        pcap(self.iface).setnonblock.assert_called_with(True)
