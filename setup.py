from distutils.core import setup, Command

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


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        subprocess.call([sys.executable, 'pytest_standalone.py', 'README.rst'])
        #errno = subprocess.call([sys.executable, 'runtests.py'])
        #raise SystemExit(errno)


if __name__=='__main__':
    assert sys.version_info[0]==3

    Info = get_info_from_readme()
    setup(
        # Information from README
        author=Info.get('author'),
        author_email='Apua.A.Aa@gmail',
        version=Info.get('version'),
        license=Info.get('copyright'),
        description=Info.get('subtitle'),
        long_description=Info.get('content'),
        name=Info.get('title').lower(),
        url=Info.get('url'),
        # Information for installation
        #package_dir={'': 'PY2' if sys.version_info[0]==2 else '.'},
        package_dir={'': '.'},
        packages=['colorprint'],
        scripts=['scripts/colorprint'],
        #test_suite='tests',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3.4',
            ],
        #test_require=['pytest'], 
        cmdclass = {'test': PyTest},
        )
