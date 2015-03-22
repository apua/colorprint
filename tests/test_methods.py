'''
# instantiate test
print(sep='\n', *attr_names.items())
pprint(attr_names)
# method generating test
print(
    print.values,
    print.red.values,
    print.red.bgcyan.values,
    sep='\n')
# print function running test
print(' ', sep=' - ', *range(10))
print.red(' ', sep=' - ', *range(10))
print.red.bgcyan(' ', sep=' - ', *range(10))

rec = []; rec.append(rec)
obj = ([0,1,{2:"3 33 333",4:{5, lambda:0}}],rec)
print.reverse(obj)
pprint.reverse(obj, indent=3, width=1)

# exception test
print.kkk
'''

from os.path import abspath, join
import sys

source_root = abspath(join(__file__, '..', '..'))
sys.path.append(source_root)


from unittest import TestCase, skip
from colorprint import (print_ as print,
                        pprint_ as pprint,
                        color_attr_mapping)


def dump_output(program):
    from contextlib import redirect_stdout
    from io import StringIO

    buff = StringIO()
    with redirect_stdout(buff):
        exec(program)
    return buff.getvalue()


class ColorPrintMethodsTest(TestCase):
    def test_no_effect(self):
        program = "print(1,2,3, sep='-', end='')"
        output = dump_output(program)
        self.assertEqual(output, '1-2-3')

    def test_with_attributes(self):
        program = "print.red.bgred(1,2, end='')"
        output = dump_output(program)
        self.assertEqual(output, '\x1b[31;41m1\x1b[m \x1b[31;41m2\x1b[m')

    def test_with_parameters(self):
        program = "print(1,2, colors=('red','bgred'), end='')"
        output = dump_output(program)
        self.assertEqual(output, '\x1b[31;41m1\x1b[m \x1b[31;41m2\x1b[m')

    def test_with_invalid_color_names(self):
        program = "print.xxx(1)"
        self.assertRaises(AttributeError, dump_output, program)

    #@skip('undefined behavior')
    def test_with_both_features(self):
        program = "print.red(1, colors={'red'})"
        self.assertRaises(TypeError, dump_output, program)

    def test_mapping_updating(self):
        color_attr_mapping['ocean'] = \
            color_attr_mapping['bright'] + (38, 5, 27)
        color_attr_mapping['fire'] = (31, 103)
        program_1 = "print.ocean(1)"
        program_2 = "print.fire(1)"
        output_1 = dump_output(program_1)
        output_2 = dump_output(program_2)
        self.assertEqual(output_1, '\x1b[1;38;5;27m1\x1b[m\n')
        self.assertEqual(output_2, '\x1b[31;103m1\x1b[m\n')
