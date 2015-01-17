from distutils.core import setup
import sys

setup(
    name='VT100-ColorPrint',
    version='2',
    description='Color print functions and command line tool',
    long_description=open('README.rst').read(),
    author='Apua',
    url='https://github.com/apua/colorprint',
    license='WTFPL',
    package_dir={'': 'PY2' if sys.version_info[0]==2 else ''}
    packages=['colorprint'],
    scripts=['scripts/colorprint'],
    )
