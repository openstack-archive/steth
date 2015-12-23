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


from stetho.common import utils as s_utils
from stetho.agent.common import utils as agent_utils


def check_ports_on_br(bridge, ports=[]):
    """ovs-vsctl list-ports bridge
    """
    pass


def ping(ips,  boardcast=False,
         count=2, timeout=2, interface=None):
    """ping host -c 2 -W 2
    packet loss
    """
    pass


def add_vlan_to_interface(interface, vlan_id):
    """ip link add link eth0 name eth0.10 type vlan id 10
    """
    subif = '%s.%s' % (interface, vlan_id)
    cmd = ['ip', 'link', 'add', 'link', interface, 'name',
           subif, 'type', 'vlan', vlan_id]
    code, data = utils.execute(cmd)


def get_interface(interface):
    """ifconfig
    """
    code, message, data = agent_utils.get_interface(interface)
    return s_utils.make_response(code, message, data)


def setup_link(interface, cidr):
    """IP addr and ifup
    check net_cidr
    10.0.0.0/24 -> 10.0.0.64/24
    """
    pass


def teardown_link(interface):
    """ip link
    """
    pass
