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


class Interface(object):

    def __init__(self, name, state=None, inet=None, netmask=None,
                 broadcast=None, ether=None):
        self.name = name
        self.inet = inet
        self.state = state
        self.netmask = netmask
        self.broadcast = broadcast
        self.ether = ether

    def make_dict(self):
        inf = dict()
        inf['name'] = self.name
        inf['inet'] = self.inet
        inf['state'] = self.state
        inf['netmask'] = self.netmask
        inf['broadcast'] = self.broadcast
        inf['ether'] = self.ether
        return inf
