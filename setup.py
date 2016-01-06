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

import sys
from setuptools import setup, find_packages
# In CentOS6.5, the version of python is 2.6, and in CentOS7 the version of
# python is 2.7. So we can according by the python version to put the
# stetho-agent script to the right place.
#
# If in CentOS6.5, the init script should be placed in "/etc/init.d/"
# If in CentOS7, the init script should be placed in "/etc/systemd/system/"
#
CENTOS6 = '/etc/init.d/'
CENTOS7 = '/etc/systemd/system/'
CENTOS6_SCRIPT = 'etc/init.d/stetho-agent'
CENTOS7_SCRIPT = 'etc/init.d/stetho-agent.service'
PYTHON_VERSION = '2.6' if '2.6' in sys.version else '2.7'
AGENT_INIT_SCRIPT = CENTOS6 if PYTHON_VERSION == '2.6' else CENTOS7
SCRIPT_LOCATION = CENTOS6_SCRIPT if PYTHON_VERSION == '2.6' else CENTOS7_SCRIPT

setup(name='stetho',
      version="0.1.0",
      packages = find_packages(),
      zip_safe = False,
      description = "stetho",
      author = "UnitedStackSDN",
      author_email = "unitedstack-sdn@googlegroups.com",
      license = "APL",
      keywords = ("stetho", "egg"),
      platforms = "Independant",
      url = "https://www.ustack.com",
      data_files=[
              ('/etc/stetho', ['etc/stetho.conf']),
             (AGENT_INIT_SCRIPT, [SCRIPT_LOCATION]),

      ],
      entry_points={
          'console_scripts': [
              'stetho = stetho.stethoclient.stethoclient.shell:main',
              'stetho-agent = stetho.agent.agent:main',
          ]
      }
)
