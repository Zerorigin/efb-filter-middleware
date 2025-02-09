import os
import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    raise Exception("Python 3.6 or higher is required. Your version is %s." % sys.version)

version_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'efb_filter_middleware/__version__.py')

__version__ = ""
exec(open(version_path).read())

long_description = open('README.md', encoding='utf-8').read()

setup(
    name='efb-filter-middleware',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=__version__,
    description='Filter middleware for EH Forwarder Bot, filter using white list and black list.',
    long_description=long_description,
    author='Zerorigin',
    author_email='871670172@qq.com',
    url='https://github.com/Zerorigin/efb-filter-middleware',
    license='GPLv3',
    include_package_data=True,
    python_requires='>=3.6',
    keywords=['ehforwarderbot', 'EH Forwarder Bot', 'EH Forwarder Bot Master Channel', 'Filter'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities"
    ],
    install_requires=[
        "ehforwarderbot"
    ],
    entry_points={
        "ehforwarderbot.middleware": "zerorigin.filter = efb_filter_middleware:FilterMiddleware"
    }
)
