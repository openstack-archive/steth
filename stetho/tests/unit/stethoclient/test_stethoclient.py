import mock
import unittest
from stetho.stethoclient import shell
from stetho.stethoclient import agent_api
from stetho.stethoclient.drivers import iperf_api


class TestStethoClientMethods(unittest.TestCase):

    def test_stethoclient_get_interface(self):
        r = (('Field', 'Value'), [])
        agent_api.GetInterface.take_action = mock.Mock(return_value=r)
        shell.main(['get-interface', 'agent-64', 'eth0'])
        self.assertEqual(agent_api.GetInterface.take_action.called, True)

    def test_stethoclient_add_vlan_to_interface(self):
        r = (('Field', 'Value'), [])
        agent_api.AddVlanToInterface.take_action = mock.Mock(return_value=r)
        shell.main(['add-vlan-to-interface', 'agent-64', 'eth0', '100'])
        self.assertEqual(agent_api.AddVlanToInterface.take_action.called, True)

    def test_stethoclient_ping(self):
        r = (('Destination', 'Packet Loss (%)'), [])
        agent_api.AgentPing.take_action = mock.Mock(return_value=r)
        shell.main(['ping', 'agent-64', '1.2.4.8'])
        self.assertEqual(agent_api.AgentPing.take_action.called, True)

    def test_stethoclient_setup_link(self):
        r = (('Field', 'Value'), [])
        agent_api.SetUpLink.take_action = mock.Mock(return_value=r)
        shell.main(['setup-link', 'agent-64', 'eth1', '192.168.10.10/24'])
        self.assertEqual(agent_api.SetUpLink.take_action.called, True)

    def test_stethoclint_check_ports_on_br(self):
        r = (('Port', 'Exists'), [])
        agent_api.CheckPortsOnBr.take_action = mock.Mock(return_value=r)
        shell.main(['check-ports-on-br', 'agent-64', 'br0', 'a'])
        self.assertEqual(agent_api.CheckPortsOnBr.take_action.called, True)

    def test_check_iperf(self):
        r = (('Field', 'Value'), [])
        iperf_api.CheckIperf.take_action = mock.Mock(return_value=r)
        shell.main(['check-iperf', 'agent-64', 'agent-64'])
        self.assertEqual(iperf_api.CheckIperf.take_action.called, True)
