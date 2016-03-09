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

import os
import re
import tempfile
import signal
import subprocess
import platform
from threading import Timer
from steth.agent.common import resource
from steth.agent.common import log
from steth.agent.common import constants

LOG = log.get_logger()


def execute(cmd, shell=False, root=False, timeout=10):
    try:
        if root:
            cmd.insert(0, 'sudo')
        LOG.info(cmd)
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
        LOG.error(e)
        raise


def execute_wait(cmd, shell=False, root=False):
    subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=shell)
    stdout, stderr = subproc.communicate()
    stdcode = subproc.returncode
    return stdcode, stdout, stderr


def create_deamon(cmd, shell=False, root=False):
    """Usage:
        Create servcice process.
    """
    try:
        if root:
            cmd.insert(0, 'sudo')
        LOG.info(cmd)
        subproc = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return subproc.pid
    except Exception as e:
        LOG.error(e)
        raise


def kill_process_by_id(pid):
    pid = int(pid)
    os.kill(pid, signal.SIGILL)
    os.waitpid(pid, 0)


def get_interface(interface):
    """Support Centos standard physical interface,
       such as eth0.
    """
    # Supported CentOS Version
    supported_dists = ['7.0', '7.1', '6.5']

    def format_centos_7(inf):
        pattern = r'<([A-Z]+)'
        state = re.search(pattern, stdout[0]).groups()[0]
        state = 'UP' if not cmp(state, 'UP') else 'DOWN'
        inf.state = state
        stdout.pop(0)
        pattern = r'inet\s(.*)\s\snetmask\s(.*)\s\sbroadcast\s(.*)'
        for line in stdout:
            if line.startswith('inet '):
                tmp = re.search(pattern, line).groups()
                (inf.inet, inf.netmask, inf.broadcast) = tmp
                stdout.remove(line)
                break
        for line in stdout:
            if line.startswith('ether'):
                inf.ether = line[6:23]
                break
        return stdcode, '', inf.make_dict()

    def format_centos_6_5(inf):
        pattern = r'HWaddr\s(.*)'
        inf.ether = re.search(pattern, stdout[0]).groups()[0]
        stdout.pop(0)
        pattern = r'addr:(.*)\s\sBcast:(.*)\s\sMask:(.*)'
        for line in stdout:
            if line.startswith('inet '):
                tmp = re.search(pattern, line).groups()
                (inf.inet, inf.broadcast, inf.netmask) = tmp
                stdout.remove(line)
                break
        inf.state = 'DOWN'
        for line in stdout:
            if 'RUNNING' in line:
                state = line[:2]
                state = 'UP' if not cmp(state, 'UP') else 'DOWN'
                inf.state = state
                break
        return stdcode, '', inf.make_dict()

    linux_dist = platform.linux_distribution()[1][:3]
    if linux_dist in supported_dists:
        try:
            cmd = ['ifconfig', interface]
            stdcode, stdout = execute(cmd)
            inf = resource.Interface(interface)
            if not cmp(linux_dist, '6.5'):
                return format_centos_6_5(inf)
            elif not cmp(linux_dist, '7.0') or not cmp(linux_dist, '7.1'):
                return format_centos_7(inf)
        except Exception:
            message = stdout.pop(0)
            return stdcode, message, None

    # Unsupported OS distribute
    message = 'Unsupported OS distribute %s, only support for CentOS %s.'
    message = message % (linux_dist, str(supported_dists))
    return 1, message, None


def register_api(server, api_obj):
    methods = dir(api_obj)
    apis = filter(lambda m: not m.startswith('_'), methods)
    [server.register_function(getattr(api_obj, api)) for api in apis]
    LOG.info("Registered api %s" % apis)


def make_response(code=0, message='', data=dict()):
    response = dict()
    response['code'] = code
    response['message'] = '' if message is None else message
    response['data'] = dict() if data is None else data
    return response


def replace_file(file_name, mode=0o644):
    base_dir = os.path.dirname(os.path.abspath(file_name))
    tmp_file = tempfile.NamedTemporaryFile('w+', dir=base_dir, delete=False)
    os.chmod(tmp_file.name, mode)
    os.rename(tmp_file.name, file_name)


def get_vif_name(prefix, port_id):
    requested_name = prefix + port_id
    return requested_name[:constants.DEVICE_NAME_LEN]
