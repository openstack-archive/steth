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
]

cfg.CONF.register_opts(OPTS)
cfg.CONF([], project='steth',
         default_config_files=['/etc/steth/steth.conf'])

AGENT_INFOS = {}
all_agents = cfg.CONF.network_agents_info + cfg.CONF.compute_agents_info
for agent in all_agents:
    item = {'agent-' + agent: cfg.CONF.managed_network_prefix + agent}
    AGENT_INFOS.update(item)
