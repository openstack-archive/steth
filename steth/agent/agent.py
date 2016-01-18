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

from SocketServer import ThreadingMixIn
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from steth.agent import api as agent_api
from steth.agent.common import utils as agent_utils
from steth.agent.common import log

# Listening endpoint
LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = 9698

LOG = log.get_logger()


class AsyncJSONRPCServer(ThreadingMixIn, SimpleJSONRPCServer):
    pass


def main():
    # log
    endpoint = (LISTEN_ADDR, LISTEN_PORT)
    server = AsyncJSONRPCServer(endpoint)
    server.register_multicall_functions()
    api = agent_api.AgentApi()
    agent_utils.register_api(server, api)
    LOG.info("Agent listening in %s:%s" % endpoint)
    server.serve_forever()


if __name__ == '__main__':
    main()
