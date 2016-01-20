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
import time
from netaddr import IPNetwork
from steth.agent.common import utils as agent_utils
from steth.agent.drivers import iperf as iperf_driver
from steth.agent.drivers import scapy_driver
from steth.agent.drivers import pcap_driver
from steth.agent.common import log
from steth.agent.common import constants

LOG = log.get_logger()


class AgentApi(object):

    def check_ports_on_br(self, bridge='br-ex', ports=['eth3']):
        """Check ports exist on bridge.

        ovs-vsctl list-ports bridge
        """
        LOG.info("RPC: check_ports_on_br bridge: %s, ports: %s" %
                 (bridge, ports))
        cmd = ['ovs-vsctl', 'list-ports', bridge]
        stdcode, stdout = agent_utils.execute(cmd, root=True)
        data = dict()
        if stdcode == 0:
            for port in ports:
                if port in stdout:
                    data[port] = True
                    stdout.remove(port)
                else:
                    data[port] = False
            return agent_utils.make_response(code=stdcode, data=data)
        # execute failed.
        message = stdout.pop(0)
        return agent_utils.make_response(code=stdcode,
                                         message=message)

    def ping(self, ips, boardcast=False,
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

    def add_vlan_to_interface(self, interface, vlan_id):
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
        # execute failed.
        message = stdout.pop(0)
        return agent_utils.make_response(code=stdcode, message=message)

    def get_interface(self, interface='eth0'):
        """Interface info.

        ifconfig interface
        """
        LOG.info("RPC: get_interface interfae: %s" % interface)
        code, message, data = agent_utils.get_interface(interface)
        return agent_utils.make_response(code, message, data)

    def setup_link(self, interface, cidr):
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

    def teardown_link(self, interface):
        """ip link
        """
        cmd = ['ip', 'link', 'delete', interface]
        stdcode, stdout = agent_utils.execute(cmd, root=True)
        if stdcode == 0:
            return agent_utils.make_response(code=stdcode)
        # execute failed.
        message = stdout.pop(0)
        return agent_utils.make_response(code=stdcode, message=message)

    def setup_iperf_server(self, protocol='TCP', port=5001, window=None):
        """iperf -s
        """
        iperf = iperf_driver.IPerfDriver()
        try:
            data = iperf.start_server(protocol='TCP', port=5001, window=None)
            return agent_utils.make_response(code=0, data=data)
        except:
            message = 'Start iperf server failed!'
            return agent_utils.make_response(code=1, message=message)

    def teardown_iperf_server(self, pid):
        iperf = iperf_driver.IPerfDriver()
        try:
            iperf.stop_server(pid)
            return agent_utils.make_response(code=0)
        except Exception as e:
            message = e.message
            return agent_utils.make_response(code=1, message=message)

    def start_iperf_client(self, host, protocol='TCP', timeout=5,
                           parallel=None, bandwidth=None, port=5001):
        iperf = iperf_driver.IPerfDriver()
        try:
            data = iperf.start_client(host, protocol='TCP', timeout=5,
                                      parallel=None, bandwidth=None)
            data['server_ip'] = host
            return agent_utils.make_response(code=0, data=data)
        except Exception as e:
            message = e.message
            return agent_utils.make_response(code=1, message=message)

    def check_dhcp_on_comp(self, port_id, port_mac,
                           phy_iface, net_type='vlan'):
        try:
            pcap = pcap_driver.PcapDriver()
            filter = '(udp and (port 68 or 67) and ether host %s)' % port_mac
            listeners = pcap.setup_listener_on_comp(port_id, filter)
            if not cmp(net_type, 'vlan'):
                phy_listener = pcap.setup_listener(phy_iface, filter)
            else:
                # TODO(yaowei) vxlan subinterface
                pass
            scapy = scapy_driver.ScapyDriver()
            scapy.send_dhcp_over_qvb(port_id, port_mac)
            # NOTE(yaowei) thread sleep 2 seconds wait for dhcp reply.
            time.sleep(2)
            map(pcap.set_nonblock, listeners)
            pcap.set_nonblock(phy_listener)
            data = dict()
            for listener in listeners:
                vif_pre = listener.name[:constants.VIF_PREFIX_LEN]
                data[vif_pre] = []
                for packet in listener.readpkts():
                    data[vif_pre].extend(scapy.get_dhcp_mt(str(packet[1])))
            data[phy_listener.name] = []
            for packet in phy_listener.readpkts():
                data[phy_listener.name].extend(
                    scapy.get_dhcp_mt(str(packet[1])))
            return agent_utils.make_response(code=0, data=data)
        except Exception as e:
            return agent_utils.make_response(code=1, message=e.message)
