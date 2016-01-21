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
import logging

FORMAT = '%(asctime)s %(filename)s %(levelname)s %(message)s'
DATEFMT = '%d %b %Y %H:%M:%S'
FILENAME = '/var/log/steth/steth-agent.log'


def get_logger(filename=FILENAME, format=FORMAT,
               datefmt=DATEFMT, filemod='a+',
               level=logging.DEBUG):
    log_dir = os.path.dirname(filename)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(level=level, format=format, datefmt=datefmt,
                        filename=filename, filemod=filemod)
    log = logging.getLogger()
    return log
