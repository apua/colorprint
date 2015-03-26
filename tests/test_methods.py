from __future__ import print_function

import os
import os.path as path
import sys
import unittest

from os.path import abspath, join

package_dir = 'PY2' if sys.version_info[0]==2 else ''
os.chdir(path.abspath(path.join(__file__, '..', '..', package_dir)))

from colorprint import (color_attr_mapping as ColorMap,
                        print_ as print, pprint_ as pprint)


def dump_output(program):
    from contextlib import redirect_stdout
    from io import StringIO

    with redirect_stdout(StringIO()) as buff:
        exec(program)
        return buff.getvalue()


class PrintMethodTest(unittest.TestCase):
    def test_no_effect(self):
        program = 'print(1,2,3, sep=\'-\', end=\'\')'
        expect_result = '1-2-3'
        self.assertEqual(dump_output(program), expect_result)

    def test_with_attributes(self):
        program = 'print.red.bgred(1,2, end=\'\')'
        expect_result = '\x1b[31;41m1\x1b[m \x1b[31;41m2\x1b[m'
        self.assertEqual(dump_output(program), expect_result)

    def test_with_parameters(self):
        program = 'print(1,2, colors=(\'red\',\'bgred\'), end=\'\')'
        expect_result ='\x1b[31;41m1\x1b[m \x1b[31;41m2\x1b[m' 
        self.assertEqual(dump_output(program), expect_result)

    def test_no_side_effect(self):
        program = 'print.bgred(1); print.blue(1)'
        expect_result = '\x1b[41m1\x1b[m\n\x1b[34m1\x1b[m\n'
        self.assertEqual(dump_output(program), expect_result)

    def test_with_invalid_color_names(self):
        program = 'print.xxx(1)'
        self.assertRaises(AttributeError, dump_output, program)

    def test_with_both_features(self):
        program = 'print.red(1, colors={\'red\'})'
        self.assertRaises(TypeError, dump_output, program)


class PPrintMethodTest(unittest.TestCase):
    def test_no_effect(self):
        program = 'pprint((1,2), width=3)'
        expect_result = '(1,\n 2)\n'
        self.assertEqual(dump_output(program), expect_result)

    def test_with_attributes(self):
        from textwrap import dedent
        program = 'pprint.red.bgred((1,2), width=3)'
        expect_result = dedent('''
            \x1b[31;41m(\x1b[m\x1b[31;41m\x1b[m\x1b[31;41m1\x1b[m\x1b[31;41m,\x1b[m
             \x1b[31;41m2\x1b[m\x1b[31;41m)\x1b[m\n
            ''')[1:-1]
        self.assertEqual(dump_output(program), expect_result)

    def test_with_parameters(self):
        from textwrap import dedent
        program = 'pprint((1,2), colors=(\'red\',\'bgred\'), width=3)'
        expect_result = dedent('''
            \x1b[31;41m(\x1b[m\x1b[31;41m\x1b[m\x1b[31;41m1\x1b[m\x1b[31;41m,\x1b[m
             \x1b[31;41m2\x1b[m\x1b[31;41m)\x1b[m\n
            ''')[1:-1]
        self.assertEqual(dump_output(program), expect_result)

    def test_no_side_effect(self):
        program = 'pprint.bgred(1); pprint.blue(1)'
        expect_result = '\x1b[41m1\x1b[m\n\x1b[34m1\x1b[m\n'
        self.assertEqual(dump_output(program), expect_result)

    def test_with_invalid_color_names(self):
        program = 'pprint.xxx(1)'
        self.assertRaises(AttributeError, dump_output, program)

    def test_with_both_features(self):
        program = 'pprint.red(1, colors={\'red\'})'
        self.assertRaises(TypeError, dump_output, program)


class ColorMapppingTest(unittest.TestCase):
    def test_mapping_updating(self):
        ColorMap['ocean'] = ColorMap['bright'] + (38, 5, 27)
        ColorMap['fire'] = (31, 103)
        program_1 = 'print.ocean(1)'
        program_2 = 'print.fire(1)'
        expect_result_1 = '\x1b[1;38;5;27m1\x1b[m\n'
        expect_result_2 = '\x1b[31;103m1\x1b[m\n'
        self.assertEqual(dump_output(program_1), expect_result_1)
        self.assertEqual(dump_output(program_2), expect_result_2)
