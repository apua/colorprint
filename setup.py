from setuptools import setup
import re
import os
import sys

def get_info_from_readme():
    """
    It is for considering additional spaces, newlines,
    and unordering docinfo of README.
    """

    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'README.rst')
    content = open(filepath).read()
    patt = r'''
        =+\n
        (?P<title>.+)\n
        =+\n+
        (?P<subtitle>.+)\n
        ~+\n+
        (?P<docinfo>
            (:[^:]+:.+\n+)
            +)
        '''
    field = r':([^:]+):\s*(.+)'
    result = re.search(patt, content, flags=re.VERBOSE).groupdict()
    result.update({
        m.group(1).lower(): m.group(2)
        for m in re.finditer(field, result['docinfo'])
        })
    return result

Info = get_info_from_readme()

setup(
    # Information from README
    author=Info.get('author'),
    version=Info.get('version'),
    license=Info.get('copyright'),
    description=Info.get('subtitle'),
    long_description=Info.get('content'),
    name=Info.get('title'),
    url=Info.get('url'),
    # Information for installation
    package_dir={'': 'PY2' if sys.version_info[0]==2 else '.'},
    packages=['colorprint'],
    scripts=['scripts/colorprint'],
    test_suite='tests',
    )
