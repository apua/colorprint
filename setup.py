from distutils.core import setup
import sys

if sys.version_info[:2] < (3, 4):
    sys.exit('virtualenv requires Python 3.4 or higher.')

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='VT100-ColorPrint',                                  
    version='1.0',                                      
    description='Color Print - VT100 Print Functions',  
    long_description=long_description,
    author='Apua',                                      
    author_email='Apua.A.Aa@gmail.com',                 
    url='https://github.com/apua/colorprint',           
    license='WTFPL',                                    
    py_modules=['colorprint'],
    )
