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
import sys
import zerorpc

# Listening endpoint
LISTEN_PROTOCOL = 'tcp'
LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = '9698'


class AgentApi(object):
    """Agent Api.
    """

    def __init__(self):
        pass

    def check_ports_on_br(self, bridge, ports=[]):
        """ovs-vsctl list-ports bridge
        """
        pass

    def ping(self, ips,  boardcast=False,
             count=2, timeout=2, interface=None):
        """ping host -c 2 -W 2
        packet loss
        """
        pass

    def add_vlan_to_interface(self, interface, vlan_id):
        """ip link add link
        """
        pass

    def get_interface_info(self, interface):
        """ifconfig
        """
        pass

    def setup_link(self, interface, cidr):
        """IP addr and ifup
        check net_cidr
        10.0.0.0/24 -> 10.0.0.64/24
        """
        pass

    def teardown_link(self, interface):
        """ip link
        """
        pass


def main():
    # log
    args = sys.argv[1:]
    s = zerorpc.Server(AgentApi())
    endpoint = '%s://%s:%s' % (LISTEN_PROTOCOL, LISTEN_ADDR, LISTEN_PORT)
    s.bind(endpoint)
    s.run()

if __name__ == '__main__':
    main()
