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

import re
from netaddr import IPNetwork
from stetho.agent.common import utils as agent_utils


def check_ports_on_br(bridge='br-ex', ports=['eth3']):
    """Check ports exist on bridge.

    ovs-vsctl list-ports bridge
    """
    cmd = ['ovs-vsctl', 'list-ports', bridge]
    stdcode, stdout = agent_utils.execute(cmd, root=True)
    data = dict()
    if not stdcode:
        for port in ports:
            if port in stdout:
                data[port] = True
                stdout.remove(port)
            else:
                data[port] = False
        return agent_utils.make_response(code=stdcode, data=data)
    else:
        message = stdout.pop(0)
        return agent_utils.make_response(code=stdcode,
                                         message=message)


def ping(ips,  boardcast=False,
         count=2, timeout=2, interface=None):
    """Ping host or broadcast.

    ping host -c 2 -W 2
    """
    cmd = ['ping', '-c', str(count), '-W', str(timeout)]
    True if not interface else cmd.extend(['-I', interface])
    True if not boardcast else cmd.append('-b')
    # Batch create subprocess
    data = dict()
    try:
        for ip in ips:
            stdcode, stdout = agent_utils.execute(cmd + [ip])
            if stdcode:
                data[ip] = 100
            else:
                pattern = r',\s([0-9]+)%\spacket\sloss'
                data[ip] = re.search(pattern, stdout[-2]).groups()[0]
        return agent_utils.make_response(code=0, data=data)
    except Exception as e:
        message = e.message
        return agent_utils.make_response(code=1, message=message)


def add_vlan_to_interface(interface, vlan_id):
    """Add vlan interface.

    ip link add link eth0 name eth0.10 type vlan id 10
    """
    subif = '%s.%s' % (interface, vlan_id)
    vlan_id = '%s' % vlan_id
    cmd = ['ip', 'link', 'add', 'link', interface, 'name',
           subif, 'type', 'vlan', 'id', vlan_id]
    stdcode, stdout = agent_utils.execute(cmd, root=True)
    if stdcode == 0:
        return agent_utils.make_response(code=stdcode)
    else:
        message = stdout.pop(0)
        return agent_utils.make_response(code=stdcode, message=message)


def get_interface(interface='eth0'):
    """Interface info.

    ifconfig interface
    """
    code, message, data = agent_utils.get_interface(interface)
    return agent_utils.make_response(code, message, data)


def setup_link(interface, cidr):
    """Setup a link.

    ip addr add dev interface
    ip link  set dev interface up
    """
    # clear old ipaddr in interface
    cmd = ['ip', 'addr', 'flush', 'dev', interface]
    agent_utils.execute(cmd, root=True)
    ip = IPNetwork(cidr)
    cmd = ['ip', 'addr', 'add', cidr, 'broadcast',
           str(ip.broadcast), 'dev', interface]
    stdcode, stdout = agent_utils.execute(cmd, root=True)
    if stdcode == 0:
        cmd = ['ip', 'link', 'set', 'dev', interface, 'up']
        stdcode, stdout = agent_utils.execute(cmd, root=True)
        if stdcode == 0:
            return agent_utils.make_response(code=stdcode)
    # execute failed.
    message = stdout.pop(0)
    return agent_utils.make_response(code=stdcode, message=message)


def teardown_link(interface):
    """ip link
    """
    cmd = ['ip', 'link', 'delete', interface]
    stdcode, stdout = agent_utils.execute(cmd, root=True)
    if stdcode == 0:
        return agent_utils.make_response(code=stdcode)
    else:
        message = stdout.pop(0)
        return agent_utils.make_response(code=stdcode, message=message)
