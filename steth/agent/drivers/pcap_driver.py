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

import pcap
from steth.agent.common import log
from steth.agent.common import utils
from steth.agent.common import constants

LOG = log.get_logger()


class PcapDriver(object):

    def setup_listener(self, iface, filter, timeout=2):
        listener = pcap.pcap(iface, timeout_ms=timeout * 1000)
        listener.setfilter(filter)
        return listener

    def setup_listener_on_comp(self, port_id, filter):
        tap_device = utils.get_vif_name(constants.TAP_DEVICE_PREFIX, port_id)
        qvb_device = utils.get_vif_name(constants.QVB_DEVICE_PREFIX, port_id)
        qbr_device = utils.get_vif_name(constants.QBR_DEVICE_PREFIX, port_id)
        qvo_device = utils.get_vif_name(constants.QVO_DEVICE_PREFIX, port_id)
        vif_devices = [tap_device, qvb_device, qbr_device, qvo_device]
        return map(lambda vif: self.setup_listener(vif, filter), vif_devices)

    def set_nonblock(self, listener):
        listener.setnonblock(True)
