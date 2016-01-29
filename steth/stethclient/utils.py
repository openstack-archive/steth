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

import logging
import jsonrpclib
import six
import socket
import sys


def safe_decode(text, incoming=None, errors='strict'):
    """Decodes incoming str using `incoming` if they're not already unicode.

    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a unicode `incoming` encoded
                representation of it.
    :raises TypeError: If text is not an isntance of str
    """
    if not isinstance(text, six.string_types):
        raise TypeError("%s can't be decoded" % type(text))

    if isinstance(text, six.text_type):
        return text

    if not incoming:
        incoming = (sys.stdin.encoding or
                    sys.getdefaultencoding())

    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        # Note(flaper87) If we get here, it means that
        # sys.stdin.encoding / sys.getdefaultencoding
        # didn't return a suitable encoding to decode
        # text. This happens mostly when global LANG
        # var is not set correctly and there's no
        # default encoding. In this case, most likely
        # python will use ASCII or ANSI encoders as
        # default encodings but they won't be capable
        # of decoding non-ASCII characters.
        #
        # Also, UTF-8 is being used since it's an ASCII
        # extension.
        return text.decode('utf-8', errors)


class Logger():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def log_normal(info):
        print Logger.OKBLUE + info + Logger.ENDC

    @staticmethod
    def log_high(info):
        print Logger.OKGREEN + info + Logger.ENDC

    @staticmethod
    def log_fail(info):
        print Logger.FAIL + info + Logger.ENDC

LISTEN_PORT = 9698

try:
    from steth.stethclient.constants import MGMT_AGENTS_INFOS
    from steth.stethclient.constants import NET_AGENTS_INFOS
    from steth.stethclient.constants import STORAGE_AGENTS_INFOS
except:
    Logger.log_fail("Import configure file fail.")
    MGMT_AGENTS_INFOS = NET_AGENTS_INFOS = STORAGE_AGENTS_INFOS = {
        'agent-64': "127.0.0.1",
        'agent-65': "127.0.0.1",
    }


def setup_server(agent):
    log = logging.getLogger(__name__)
    if agent in MGMT_AGENTS_INFOS:
        log.debug('get agent:%s ip_address:%s' % (
            agent, MGMT_AGENTS_INFOS[agent]))
    else:
        log.error('Agent %s not configured. Please check it.' % (agent))
        sys.exit()
    log.debug('Begin create connection with http://%s:%s.' % (
        agent,
        LISTEN_PORT))
    server = jsonrpclib.Server('http://%s:%s' %
                               (MGMT_AGENTS_INFOS[agent], LISTEN_PORT))
    log.debug('Create connection with %s success.' % (agent))
    return server


def is_ip(addr):
    try:
        socket.inet_aton(addr)
        # legal
        return 0
    except socket.error:
        # Not legal
        return 1


def get_ip_from_agent(node, net_type):
    from steth.stethclient.constants import MGMT_TYPE
    from steth.stethclient.constants import NET_TYPE
    from steth.stethclient.constants import STORAGE_TYPE
    try:
        if net_type == NET_TYPE:
            return NET_AGENTS_INFOS[node]
        elif net_type == MGMT_TYPE:
            return MGMT_AGENTS_INFOS[node]
        elif net_type == STORAGE_TYPE:
            return STORAGE_AGENTS_INFOS[node]
        else:
            return 1
    except Exception as e:
        print "Can't get ip! Because: %s" % e
