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

import struct
from scapy import all as scapy
from steth.agent.common import log
from steth.agent.common import utils
from steth.agent.common import constants

LOG = log.get_logger()
scapy.conf.checkIPaddr = False


class ScapyDriver(object):

    def send_dhcp_over_qvb(self, port_id, port_mac):
        """Send DHCP Discovery over qvb device.
        """
        qvb_device = utils.get_vif_name(constants.QVB_DEVICE_PREFIX, port_id)
        ethernet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff',
                               src=port_mac, type=0x800)
        ip = scapy.IP(src='0.0.0.0', dst='255.255.255.255')
        udp = scapy.UDP(sport=68, dport=67)
        port_mac_t = tuple(map(lambda x: int(x, 16), port_mac.split(':')))
        hw = struct.pack('6B', *port_mac_t)
        bootp = scapy.BOOTP(chaddr=hw, flags=1)
        dhcp = scapy.DHCP(options=[("message-type", "discover"), "end"])
        packet = ethernet / ip / udp / bootp / dhcp
        scapy.sendp(packet, iface=qvb_device)

    def get_dhcp_mt(self, buff):
        """Pick out DHCP Message Type from buffer.
        """
        ether_packet = scapy.Ether(buff)
        dhcp_packet = ether_packet[scapy.DHCP]
        # ('message-type', 1)
        message = dhcp_packet.options[0]
        return constants.DHCP_MESSATE_TYPE[message[1]]

    def get_arp_op(self, buff):
        ether_packet = scapy.Ether(buff)
        arp_packet = ether_packet[scapy.ARP]
        return constants.ARP_OP_TYPE[arp_packet.op]
