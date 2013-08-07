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
    # classifiers=[
    # ],
    scripts=['pycommand-example'],
)
