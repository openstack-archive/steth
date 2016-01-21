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

# Virtuel Interface Prefix
TAP_DEVICE_PREFIX = 'tap'
QBR_DEVICE_PREFIX = 'qbr'
QVB_DEVICE_PREFIX = 'qvb'
QVO_DEVICE_PREFIX = 'qvo'

VIF_PREFIX_LEN = 3
DEVICE_NAME_LEN = 14

# DHCP Message Type
# Reference: http://www.networksorcery.com/enp/rfc/rfc1533.txt
DHCP_MESSATE_TYPE = ['', 'DHCPDISCOVER', 'DHCPOFFER', 'DHCPREQUEST',
                     'DHCPDECLINE', 'DHCPACK', 'DHCPNAK', 'DHCPRELEASE']
DHCP_NS_PREFIX = 'qdhcp-'

# Reference: http://www.networksorcery.com/enp/rfc/rfc826.txt
ARP_OP_TYPE = ['', 'REQUEST', 'REPLY']
