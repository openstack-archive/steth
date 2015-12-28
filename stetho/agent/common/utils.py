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
from stetho.agent.common import resource


def execute(cmd, shell=False, root=False, timeout=10):
    try:
        if root:
            cmd.insert(0, 'sudo')
        subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=shell)
        timer = Timer(timeout, lambda proc: proc.kill(), [subproc])
        timer.start()
        subproc.wait()
        stdcode = subproc.returncode
        stdout = subproc.stdout.readlines()
        stderr = subproc.stderr.readlines()
        timer.cancel()

        def list_strip(lines):
            return [line.strip() for line in lines]

        return stdcode, list_strip(stderr) if stdcode else list_strip(stdout)
    except Exception as e:
        raise


def get_interface(interface):
    """Support Centos standard physical interface,
       such as eth0.
    """
    cmd = ['ifconfig', interface]
    stdcode, stdout = execute(cmd)
    try:
        inf = resource.Interface(interface)
        pattern = r'<([A-Z]+)'
        inf.state = re.search(pattern, stdout[0]).groups()[0]
        pattern = r'inet\s(.*)\s\snetmask\s(.*)\s\sbroadcast\s(.*)'
        for line in stdout:
            if line.startswith('inet '):
                tmp = re.search(pattern, stdout[1]).groups()
                (inf.inet, inf.netmask, inf.broadcast) = tmp
                stdout.remove(line)
                break
        for line in stdout:
            if line.startswith('ether'):
                inf.ether = line[6:23]
                stdout.remove(line)
                break
        return stdcode, '', inf.make_dict()
    except Exception as e:
        message = stdout.pop(0)
        return stdcode, message, None


def register_api(server, api_obj):
    methods = dir(api_obj)
    apis = filter(lambda m: not m.startswith('_'), methods)
    [server.register_function(getattr(api_obj, api)) for api in apis]


def make_response(code=0, message='', data=dict()):
    response = dict()
    response['code'] = code
    response['message'] = '' if message is None else message
    response['data'] = dict() if data is None else data
    return response
