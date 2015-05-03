#!/usr/bin/env python
# coding: utf-8
''' Zhudi provides a Chinese - language dictionnary based on the
    C[E|F]DICT project Copyright - 2011-2015 - Ma Jiehong

    Zhudi is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Zhudi is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
    License for more details.

    You should have received a copy of the GNU General Public License
    If not, see <http://www.gnu.org/licenses/>.

'''
import unittest

# Add here the part you want to test if it is a new one
import zhudi

class TestCommandLineProcessing(unittest.TestCase):

    def test_splitting_with_gui(self):
        from subprocess import Popen, PIPE
        with Popen(["sh",
                    "scripts/zhudi",
                    "-s",
                    "dict_test.u8"], stdout=PIPE, stderr=PIPE) as proc:
            return_code = proc.returncode
        self.assertEqual(return_code, None)

    def test_splitting_with_cli(self):
        from subprocess import Popen, PIPE
        with Popen(["sh",
                    "scripts/zhu",
                    "-s",
                    "dict_test.u8",
                    "''"], stdout=PIPE, stderr=PIPE) as proc:
            return_code = proc.returncode
        self.assertEqual(return_code, None)

if __name__ == '__main__':
    unittest.main()
