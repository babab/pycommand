pycommand 0.3.0
******************************************************************************

.. image:: https://travis-ci.org/babab/pycommand.svg?branch=master
    :target: https://travis-ci.org/babab/pycommand

**A clean and simplistic alternative for argparse, optparse and getopt**

Pycommand is essentially a fancy wrapper around getopt that consists of
one simple `CommandBase` class that you can use to create executable
commands for your python programs with very simplistic and readable
code. It has support for subcommands and also nesting commands, so you
can create (multiple levels of) subcommands, with the ability to pass
the values of optional arguments of a command object to its subcommand
objects. Supported Python versions are 2.7 and 3.2 and later.

- PyPI: https://pypi.python.org/pypi/pycommand/
- User and API docs: http://pythonhosted.org/pycommand/
- Bitbucket: https://bitbucket.org/babab/pycommand
- Github: https://github.com/babab/pycommand

.. note::

   This README reflects the development version. For the latest release
   documentation, visit http://pythonhosted.org/pycommand/


Download and install
====================

If you have pip installed, you can just:

.. code-block:: console

   # pip install pycommand

To work with the current development version, do something like this:

.. code-block:: console

   $ git clone git://bitbucket.org/babab/pycommand.git
   # cd pycommand
   # pip install --upgrade -e .


Quick setup from a template
===========================

To quicly start writing a command from a template (much like the
examples below), use pycommand's helper script by running:

.. code-block:: console

   $ pycommand init

This will ask you for an executable name, class name and template type
and it will save it to an executable file, ready to be used as a Python
shell script (for your Python package/module)).


Example
=======

For full documentation and examples, visit http://pythonhosted.org/pycommand/

Here is an undocumented code example of getting automated usage text
generation and parsing of optional arguments. If we name the script
for which you can see the code below ``basic-example`` and execute it,
the following will be the output for running ``basic-example -h`` or
``basic-example --help``:

.. code-block:: console

   usage: basic-example [options]

   An example of a basic CLI program

   Options:
   -h, --help                        show this help information
   -f <filename>, --file=<filename>  use specified file
   --version                         show version information

And here is the code:

.. code-block:: python

   #!/usr/bin/env python

   import pycommand
   import sys


   class BasicExampleCommand(pycommand.CommandBase):
       '''An example of a basic CLI program'''
       usagestr = 'usage: basic-example [options]'
       description = __doc__

       optionList = (
           ('help', ('h', False, 'show this help information')),
           ('file', ('f', '<filename>', 'use specified file')),
           ('version', ('', False, 'show version information')),
       )

       def run(self):
           if self.flags.help:
               print(self.usage)
               return 0
           elif self.flags.version:
               print('Python version ' + sys.version.split()[0])
               return 0
           elif self.flags.file:
               print('filename = ' + self.flags.file)
               return 0

           print('Program completed. Try adding "--help"')

   if __name__ == '__main__':
       # Shortcut for reading from sys.argv[1:] and sys.exit(status)
       pycommand.run_and_exit(BasicExampleCommand)

       # The shortcut is equivalent to the following:

       # cmd = BasicExampleCommand(sys.argv[1:])
       # if cmd.error:
       #     print('error: {0}'.format(cmd.error))
       #     sys.exit(1)
       # else:
       #     sys.exit(cmd.run())


Why was it created?
===================

When parsing command line program arguments, I sometimes work with
`argparse` (a replacement for `optparse`). I don't really like the API
and the output it gives, which is the main reason I've always used
`getopt` for parsing arguments whenever possible.

The `CommandBase` class was originally written for *DisPass*,
which is a password manager/generator, as a means to easily define new
subcommands and have auto-generated usage messages. Because I want to
have this in other projects I've decided to put it in the cheeseshop.


Software license
================

Copyright (c) 2013-2015  Benjamin Althues <benjamin@babab.nl>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
