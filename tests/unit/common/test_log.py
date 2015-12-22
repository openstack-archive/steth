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

import unittest
import logging

from stetho.common import log


class TestLog(unittest.TestCase):
    def test_get_logger(self):
        log_test = log.get_logger(filename='test')
        self.assertEqual(type(log_test), type(logging.getLogger()))

if __name__ == '__main__':
    unittest.main()
