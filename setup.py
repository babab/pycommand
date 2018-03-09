from setuptools import setup
import pycommand

setup(
    name='pycommand',
    version=pycommand.__version__,
    description=pycommand.__doc__,
    author=pycommand.__author__,
    author_email='benjamin@althu.es',
    url='https://github.com/babab/pycommand',
    download_url='http://pypi.python.org/pypi/pycommand/',
    py_modules=['pycommand'],
    license='ISC',
    long_description='{}\n{}'.format(open('README.rst').read(),
                                     open('CHANGELOG.rst').read()),
    platforms='any',
    scripts=['scripts/pycommand'],
    data_files=[
        ('share/pycommand/examples', ['examples/basic-example',
                                      'examples/full-example']),
        ('share/pycommand', ['LICENSE', 'README.rst']),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Shells',
        'Topic :: System :: Software Distribution',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
