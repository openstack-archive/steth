import mock
import unittest
from stetho.agent import api
from stetho.stethoclient import shell
from stetho.stethoclient import agent_api
from stetho.stethoclient.drivers import iperf_api


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

class TestStethoClientMethods(unittest.TestCase):

    def setUp(self):
        self.server = Server()
        agent_api.setup_server = mock.Mock(return_value=self.server)
        iperf_api.setup_server = mock.Mock(return_value=self.server)

    def test_stethoclient_get_interface(self):
        r =  {'message': '', 'code': 0, 'data': {'name': 'eth0'}}
        self.server.get_interface = mock.Mock(return_value=r)
        shell.main(['get-interface', 'agent-64', 'eth0'])
        self.assertEqual(self.server.get_interface.called, True)

    def test_stethoclient_add_vlan_to_interface(self):
        r = {u'message': '', 'code': 0, 'data': {}}
        rr =  {'message': '', 'code': 0, 'data': {'name': 'eth0'}}
        self.server.add_vlan_to_interface = mock.Mock(return_value=r)
        self.server.get_interface = mock.Mock(return_value=rr)
        shell.main(['add-vlan-to-interface', 'agent-64', 'eth0', '100'])
        self.assertEqual(self.server.add_vlan_to_interface.called, True)

    def test_stethoclient_ping(self):
        r = {u'message': '', 'code': 0, 'data': {'1.2.4.8': 100}}
        self.server.ping = mock.Mock(return_value=r)
        shell.main(['ping', 'agent-64', '1.2.4.8'])
        self.assertEqual(self.server.ping.called, True)

    def test_stethoclient_setup_link(self):
        r = {u'message': '', 'code': 0, 'data': {}}
        rr =  {'message': '', 'code': 0, 'data': {'name': 'eth0'}}
        self.server.get_interface = mock.Mock(return_value=rr)
        self.server.setup_link = mock.Mock(return_value=r)
        shell.main(['setup-link', 'agent-64', 'eth1', '192.168.10.10/24'])
        self.assertEqual(self.server.setup_link.called, True)

    def test_stethoclint_check_ports_on_br(self):
        r = {u'message': '', 'code': 0, 'data': {'ovs_port': True}}
        self.server.check_ports_on_br = mock.Mock(return_value=r)
        shell.main(['check-ports-on-br', 'agent-64', 'br0', 'ovs_port'])
        self.assertEqual(self.server.check_ports_on_br.called, True)

    def test_check_iperf(self):
        iperf_server_r = {u'message': u'', u'code': 0, u'data': {u'pid': 1234}}
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
        teardown_iperf_r = {u'message': u'', u'code': 0, u'data': {}}
        self.server.setup_iperf_server = mock.Mock(return_value=iperf_server_r)
        self.server.start_iperf_client = mock.Mock(return_value=iperf_client_r)
        self.server.teardown_iperf_server = mock.Mock(
                                            return_value=teardown_iperf_r)
        shell.main(['check-iperf', 'agent-64', 'agent-64'])
        self.assertEqual(self.server.setup_iperf_server.called, True)
        self.assertEqual(self.server.start_iperf_client.called, True)
        self.assertEqual(self.server.teardown_iperf_server.called, True)
