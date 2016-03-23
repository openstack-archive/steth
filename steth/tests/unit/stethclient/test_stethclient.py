import mock
import unittest
from steth.stethclient import shell
from steth.stethclient import agent_api
from steth.stethclient.drivers import dhcp
from steth.stethclient.drivers import iperf_api


class Server(object):

    def get_interface(self):
        pass

    def add_vlan_to_interface(self):
        pass

    def ping(self):
        pass

    def setup_link(self):
        pass

    def check_ports_on_br(self):
        pass

    def setup_iperf_server(self):
        pass

    def start_iperf_client(self):
        pass

    def teardown_iperf_server(self):
        pass

    def check_dhcp_on_comp(self):
        pass


class TestStethClientMethods(unittest.TestCase):

    def setUp(self):
        self.server = Server()
        agent_api.setup_server = mock.Mock(return_value=self.server)
        iperf_api.setup_server = mock.Mock(return_value=self.server)
        dhcp.setup_server = mock.Mock(return_value=self.server)

    def test_stethclient_get_interface(self):
        r = {'message': '', 'code': 0, 'data': {'name': 'eth0'}}
        self.server.get_interface = mock.Mock(return_value=r)
        shell.main(['get-interface', 'agent-64', 'eth0'])
        self.assertEqual(self.server.get_interface.called, True)

    def test_stethclient_add_vlan_to_interface(self):
        r = {'message': '', 'code': 0, 'data': {}}
        rr = {'message': '', 'code': 0, 'data': {'name': 'eth0'}}
        self.server.add_vlan_to_interface = mock.Mock(return_value=r)
        self.server.get_interface = mock.Mock(return_value=rr)
        shell.main(['add-vlan-to-interface', 'agent-64', 'eth0', '100'])
        self.assertEqual(self.server.add_vlan_to_interface.called, True)

    def test_stethclient_ping(self):
        r = {'message': '', 'code': 0, 'data': {'1.2.4.8': 100}}
        self.server.ping = mock.Mock(return_value=r)
        shell.main(['ping', 'agent-64', '1.2.4.8'])
        self.assertEqual(self.server.ping.called, True)

    def test_stethclient_setup_link(self):
        r = {'message': '', 'code': 0, 'data': {}}
        rr = {'message': '', 'code': 0, 'data': {'name': 'eth0'}}
        self.server.get_interface = mock.Mock(return_value=rr)
        self.server.setup_link = mock.Mock(return_value=r)
        shell.main(['setup-link', 'agent-64', 'eth1', '192.168.10.10/24'])
        self.assertEqual(self.server.setup_link.called, True)

    def test_stethclint_check_ports_on_br(self):
        r = {'message': '', 'code': 0, 'data': {'ovs_port': True}}
        self.server.check_ports_on_br = mock.Mock(return_value=r)
        shell.main(['check-ports-on-br', 'agent-64', 'br0', 'ovs_port'])
        self.assertEqual(self.server.check_ports_on_br.called, True)

    def test_check_iperf(self):
        validate_ip_r = {'message': u'', 'code': 0, 'data': {}}
        iperf_server_r = {'message': '', 'code': 0, 'data': {'pid': 1234}}
        iperf_client_r = {
            'message': '',
            'code': 0,
            'data': {
                'Transfer': '1 GBytes',
                'Bandwidth': '1 Gbits/sec',
                'Interval': '5.0',
                'server_ip': 'localhost'
            }
        }
        teardown_iperf_r = {'message': '', 'code': 0, 'data': {}}
        self.server.setup_iperf_server = mock.Mock(return_value=iperf_server_r)
        self.server.start_iperf_client = mock.Mock(return_value=iperf_client_r)
        self.server.validate_ip = mock.Mock(return_value=validate_ip_r)
        self.server.teardown_iperf_server = mock.Mock(
            return_value=teardown_iperf_r)
        shell.main(['check-iperf', 'agent-64', 'agent-64', 'mgmt'])
        self.assertEqual(self.server.setup_iperf_server.called, True)
        self.assertEqual(self.server.start_iperf_client.called, True)
        self.assertEqual(self.server.teardown_iperf_server.called, True)

    @mock.patch('neutronclient.v2_0.client.Client.show_port')
    def test_check_dhcp_on_comp(self, show_port):
        show_port.return_value = {
            'port': {
                'mac_address': 'aa:bb:cc:dd:ee:ff',
                'binding:host_id': 'server-9'
            }
        }
        device = "tapaaaaaaaa-aa"
        msg = device + "No such device exists (SIOCGIFHWADDR: No such device)"
        check_dhcp_on_comp_r = {
            'message': msg,
            'code': 1,
            'data': {}
        }
        self.server.check_dhcp_on_comp = mock.Mock(
            return_value=check_dhcp_on_comp_r)
        shell.main(['check-dhcp-on-comp',
                    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                    'eth0', 'vlan'])
        self.assertEqual(self.server.check_dhcp_on_comp.called, True)

    @mock.patch('neutronclient.v2_0.client.Client.show_port')
    def test_check_dhcp_on_net(self, show_port):
        show_port.return_value = {
            'port': {
                'mac_address': 'aa:bb:cc:dd:ee:ff',
                'binding:host_id': 'server-9',
                'network_id': '0912af24-4525-4737-beb7-c77aa14e0567',
                'fixed_ips': [
                    {
                        'subnet_id': '73b19b70-c469-473a-b589-459524f2c6a6',
                        'ip_address': u'10.0.0.3'
                    }]
            }
        }
        device = "tapaaaaaaaa-aa"
        msg = device + "No such device exists (SIOCGIFHWADDR: No such device)"
        check_dhcp_on_net_r = {
            'message': msg,
            'code': 1,
            'data': {}
        }
        self.server.check_dhcp_on_net = mock.Mock(
            return_value=check_dhcp_on_net_r)
        shell.main(['check-dhcp-on-net',
                    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                    'eth0', 'vlan'])
        self.assertEqual(self.server.check_dhcp_on_net.called, True)
