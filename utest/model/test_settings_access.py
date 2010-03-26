#  Copyright 2008 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

from robot.utils.asserts import assert_equals

from robotide.model.settings import _Setting
from robotide.model.settings import *
from resources import FakeSuite


class TestGetStrValue(unittest.TestCase):

    def setUp(self):
        self.s = _Setting(FakeSuite())

    def test_get_value(self):
        self.s.value = ['some', 'data']
        assert_equals(self.s.get_str_value(), 'some | data')

    def test_get_empty_value(self):
        self.s.value = []
        assert_equals(self.s.get_str_value(), '')

    def test_get_none_value(self):
        self.s.value = None
        assert_equals(self.s.get_str_value(), '')

    def test_one_value(self):
        self.s.value = ['my cool value']
        assert_equals(self.s.get_str_value(), 'my cool value')

    def test_escaping_value(self):
        self.s.value = ['pipes | here', '|', '||']
        assert_equals(self.s.get_str_value(), 'pipes \\| here | \\| | \\|\\|')

    def test_empty_strings_in_value(self):
        self.s.value = ['', 'foo', '', '', 'pipe|', '']
        assert_equals(self.s.get_str_value(), ' | foo |  |  | pipe\\| | ')


class TestSetStrValue(unittest.TestCase):

    def setUp(self):
        self.s = _Setting(FakeSuite())

    def test_empty_value(self):
        self.s.set_str_value('')
        assert_equals(self.s.value, [])

    def test_one_value(self):
        self.s.set_str_value('one value')
        assert_equals(self.s.value, ['one value'])

    def test_multiple_values(self):
        self.s.set_str_value('3|values|here')
        assert_equals(self.s.value, ['3', 'values', 'here'])

    def test_values_with_spaces_around_separator(self):
        self.s.set_str_value(' 5 |  values | here|?  ')
        assert_equals(self.s.value, ['5', 'values', 'here', '?'])

    def test_empty_strins_in_values(self):
        self.s.set_str_value('|2nd||| 5th ||')
        assert_equals(self.s.value, ['', '2nd', '', '', '5th', '', ''])

    def test_unescaping(self):
        for inp, exp in [ (r'\|', ['|']),           (r'\|x', ['|x']),
                          (r'\||', ['|', '']),      (r'\||x', ['|', 'x']),
                          (r'\\|', [r'\\', '']),    (r'\\|x', [r'\\', 'x']),
                          (r'\\\|', [r'\\|']),      (r'\\\| x', [r'\\| x']),
                          (r'\\\\|', [r'\\\\', '']),
                          (r'\\ |', [r'\\', '']),
                          (r'c:\\sanity\\|\\|\|?',
                           [r'c:\\sanity\\', r'\\', '|?']) ]:
            self.s.set_str_value(inp)
            assert_equals(self.s.value, exp, inp)

    def test_concrete_implementations(self):
        for cls in [ForceTags, DefaultTags, Tags, TestSetup, TestTeardown,
                    Setup, Teardown, SuiteSetup, SuiteTeardown, TestTimeout,
                    Timeout, Arguments, ReturnValue,
                    LibraryImport, VariablesImport]:
            setting = cls(FakeSuite())
            setting.set_str_value('Foo | Bar')
            assert_equals(setting.value, ['Foo', 'Bar'])

if __name__ == '__main__':
    unittest.main()
