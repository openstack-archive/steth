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

from oslo_config import cfg

OPTS = [
    cfg.ListOpt('network_agents_info', default=[],
                help="Mappings of network agents and steth listened IP."),
    cfg.ListOpt('compute_agents_info', default=[],
                help="Mappings of compute agents and steth listened IP."),
    cfg.StrOpt('managed_network_prefix', default='127.0.0.',
               help="Managed network prefix."),
    cfg.ListOpt('networks_prefix', default=['127.0.0.', '192.168.10.'],
                help="Networks prefix."),
    cfg.StrOpt('node_name_prefix', default='server-',
               help="Prefix of every node."),
]

cfg.CONF.register_opts(OPTS)
cfg.CONF([], project='steth',
         default_config_files=['/etc/steth/steth.conf'])

all_agents = cfg.CONF.network_agents_info + cfg.CONF.compute_agents_info

# We use STETH_AGENT_INFOS to create connection to every node
STETH_AGENT_INFOS = {}

# We use ALL_AGENT_INFOS to process iperf
ALL_AGENT_INFOS = {}
for agent in all_agents:
    l = []
    prefix = cfg.CONF.networks_prefix[0]
    item = {cfg.CONF.node_name_prefix + agent: prefix + agent}
    STETH_AGENT_INFOS.update(item)
    for prefix in cfg.CONF.networks_prefix[1:]:
        l.append(prefix + agent)
        item = {cfg.CONF.node_name_prefix + agent: l}
        ALL_AGENT_INFOS.update(item)
