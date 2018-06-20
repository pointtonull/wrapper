r"""
              ,.- 'Y _^-,
               ,.-'^P E R-^ ^-,\
          ,.-'^ A P ,.-^       \|
          \ W R ,.-^            k
           \,.-^                 i
                                 ss
                                 kis
                                skiss
                                kissk
                               isskiss
                              kisskisskis
                           skisskisskisski
                        sskisskisskisskissk
                      isskisskisskisskisskiss
                   kisskisskisskisskisskisskis
              skisskisskisskisskisskisskisskiss
            kisskisskisskisskisskisskisskisskissk
           isskisskisskisskisskisskisskisskisskiss
          kisskisskisskisskisskisskisskisskisskiss
           kisskisskisskisskisskisskisskisskisskis
            skisskisskisskisskisskisskisskisskiss
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="Wrapper",
    version='0.5',
    description='Universal API Wrapper.',
    long_description=open("README.md").read(),

    url='https://github.com/pointtonull/wrapper',
    author='Carlos M. Cabrera',
    author_email='point.to+wrappe@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords="api wrapper instrocpective discover serverless notebook jupyter",
#    packages=["src/wrapper"],
    package_dir={"": "src"},
    py_modules=["wrapper", "gatekeeper"],
#    namespace_packages=["src"],
    install_requires=['requests']
)
