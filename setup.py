from distutils.core import setup
import pycommand

setup(
    name='pycommand',
    version=pycommand.__version__,
    description=pycommand.__doc__,
    author=pycommand.__author__,
    author_email='benjamin@babab.nl',
    url='http://babab.nl/',
    download_url='http://pypi.python.org/pypi/pycommand/',
    py_modules=['pycommand'],
    license='ISC',
    long_description=pycommand.long_description,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Shells',
        'Topic :: System :: Software Distribution',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
    scripts=['pycommand-example'],
)
