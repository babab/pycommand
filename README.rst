pycommand 0.3.0
******************************************************************************

.. image:: https://travis-ci.org/babab/pycommand.svg?branch=master
    :target: https://travis-ci.org/babab/pycommand
    :alt: Build Status

.. image:: https://gemnasium.com/babab/pycommand.svg
   :target: https://gemnasium.com/babab/pycommand

.. image:: https://badge.waffle.io/babab/pycommand.png?label=ready&title=Ready
   :target: https://waffle.io/babab/pycommand
   :alt: Stories in Ready

**Library / toolkit for creating command line programs with minimal effort.**

Pycommand is essentially a fancy wrapper around getopt that consists of
one simple `CommandBase` class that you can inherit to create executable
commands for your (Python) programs with very simplistic and readable
code. It has support for subcommands and also nesting commands, so you
can create (multiple levels of) subcommands, with the ability to pass
the values of optional arguments of a command object to its subcommand
objects. Supported Python versions are 2.7 and 3.2 and later.

- Documentation: http://pythonhosted.org/pycommand/
- PyPI: https://pypi.python.org/pypi/pycommand/

- Github: https://github.com/babab/pycommand
- Bitbucket: https://bitbucket.org/babab/pycommand


Features
========

- Parsing of optional and positional arguments
- Minimalistic approach with a clean API
- Create scripts in a matter of minutes using the code generator
- Auto compiled usage messages
- Graceful semi-automatic handling of exit status codes
- Subcommands can have subcommands that can have subcommands
  (each with their own optional arguments)
- Pass values for --some-option from a parent command into child commands.


Download and install
====================

If you have pip installed, you can just do:

.. code-block:: console

   # pip install pycommand


Script generator
================

To quickly start writing a command from a template (much like the
examples below), use the script generator by running:

.. code-block:: console

   $ python -m pycommand init

This will ask you for an executable name, class name and template type
and it will save it to an executable python script, ready to be used as
a command line program.

You can have a very basic command line program that handles ``-v,
--version`` and ``-h, --help`` arguments set up in less than a minute.


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
have this in other projects I've decided to put it in the cheeseshop in 2013.
It has since been refined for more generic usage and has proven to be
stable and workable throughout the years.


Software license
================

Copyright (c) 2013-2016, 2018 Benjamin Althues <benjamin@babab.nl>

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
