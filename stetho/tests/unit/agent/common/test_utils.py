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

from stetho.agent.common import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_file = self.get_temp_file_path('test_execute.tmp')
        open(self.test_file, 'w+').close()

    def test_execute(self):
        expected = "%s\n" % self.test_file
        code, result = utils.execute(["ls", self.test_file])
        self.assertEqual(0, code)
        self.assertEqual(result.pop(), expected.strip('\n'))

    def get_temp_file_path(self, filename, root=None):
        root = '/tmp/%s'
        return root % filename

    def test_make_response(self):
        para = dict()
        para['code'] = 0
        para['message'] = 'Test make response.'
        para['data'] = dict()
        result = utils.make_response(para['code'], para['message'],
                                     para['data'])
        self.assertEqual(para, result)
