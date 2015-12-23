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
import shlex
import subprocess
from threading import Timer
from stetho.common import log
from stetho.common import resource


log = log.get_logger('/var/log/stetho/stetho-agent.log')


def execute(cmd, shell=False, root=False, timeout=10):
    try:
        log.debug(cmd)
        subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
        timer = Timer(timeout, lambda proc: proc.kill(), [subproc])
        timer.start()
        subproc.wait()
        stdcode = subproc.returncode
        stdout = subproc.stdout.readlines()
        timer.cancel()
        return stdcode, [line.strip() for line in stdout]
    except Exception as e:
        log.exception(e)
        raise


def get_interface(interface):
    cmd = ['ifconfig', interface]
    stdcode, stdout = execute(cmd)
    if stdcode == 0:
        inf = resource.Interface(interface)
        pattern = r'<([A-Z]+)'
        inf.state = re.search(pattern, stdout[0]).groups()[0]
        pattern = r'inet\s(.*)\s\snetmask\s(.*)\s\sbroadcast\s(.*)'
        tmp = re.search(pattern, stdout[1]).groups()
        (inf.inet, inf.netmask, inf.broadcast) = tmp
        inf.ether = stdout[3][6:23]
        return stdcode, '', inf.make_dict()
    else:
        return stdcode, stdout.pop(), None
