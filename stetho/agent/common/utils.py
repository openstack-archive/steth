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

import time
import shlex
import subprocess
from stetho.common import log

log = log.get_logger('/opt/stack/logs/stetho-agent.log')


def execute(cmd, time=None, shell=False):
    try:
        log.info(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
        out = p.stdout.readlines()
        return [line.strip() for line in out]
    except Exception as e:
        log.exception(e)
