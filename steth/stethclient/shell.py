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
"""
Command-line interface to Steth APIs
"""

import sys

from cliff import app
from cliff import commandmanager
from steth.stethclient import agent_api
from steth.stethclient.drivers import dhcp
from steth.stethclient.drivers import iperf_api
from steth.stethclient import utils


VERSION = '0.1'
STETH_API_VERSION = '0.1'

COMMAND_V1 = {
    'setup-link': agent_api.SetUpLink,
    'teardown-link': agent_api.TearDownLink,
    'add-vlan-to-interface': agent_api.AddVlanToInterface,
    'ping': agent_api.AgentPing,
    'check-ports-on-br': agent_api.CheckPortsOnBr,
    'get-interface': agent_api.GetInterface,
    'check-vlan-interface': agent_api.CheckVlanInterface,
    'check-iperf': iperf_api.CheckIperf,
    'check-dhcp-on-comp': dhcp.CheckDHCPonComputeNodes,
    'check-dhcp-on-network': dhcp.CheckDHCPonNetworkNodes,
    'print-agents-info': agent_api.PrintAgentsInfo,
}

COMMANDS = {'0.1': COMMAND_V1}


class StethShell(app.App):

    def __init__(self, apiversion):
        super(StethShell, self).__init__(
            description=__doc__.strip(),
            version=VERSION,
            command_manager=commandmanager.CommandManager('steth.cli'),
        )
        self.commands = COMMANDS
        for k, v in self.commands[apiversion].items():
            self.command_manager.add_command(k, v)

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    try:
        return StethShell(STETH_API_VERSION).run(
            map(utils.safe_decode, argv))
    except KeyboardInterrupt:
        print "... terminating neutron client"
        return 1
    except Exception as e:
        print(e)
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
