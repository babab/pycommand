.. image:: https://travis-ci.org/babab/pycommand.svg?branch=master
    :target: https://travis-ci.org/babab/pycommand


pycommand
******************************************************************************

**Parse command line arguments / define (sub)commands with minimal code**

Pycommand consists of one simple `CommandBase` class that you can use to
create executable commands for your python programs with very simplistic
and readable code. It has support for nesting commands, so you can
create (multiple levels of) subcommands, with the ability to pass the
values of optional arguments of a command object to its subcommand
objects. Supported Python versions are 2.7, 3.2, 3.3 and 3.4

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

Download and install
====================

If you have pip installed, you can just::

   # pip install pycommand

Otherwise, do something like this::

   $ git clone git://bitbucket.org/babab/pycommand.git
   # cd pycommand
   # python setup.py install


Quick setup from a template
===========================

*(currently only available in the git version)*

To quicly start writing a command from a template (much like the
example below), just run::

   $ pycommand init

This will ask you for an executable name, class name and template type
and it will save it to an executable file, ready to be used as a Python
shell script (for your Python package/module)).


Example
=======

For full documentation and examples, visit http://pythonhosted.org/pycommand/

Here is a little preview::

   #!/usr/bin/env python

   import pycommand
   import sys


   class Command(pycommand.CommandBase):
       usagestr = 'usage: example-command [options]'
       description = 'An example of a basic CLI program'
       optionList = (
           ('help', ('h', False, 'show this help information')),
           ('file', ('f', '<filename>', 'use specified file')),
           ('version', ('', False, 'show version information')),
       )

       def run(self):
           if self.flags['help']:
               print(self.usage)
               return
           elif self.flags['version']:
               print('Python version ' + sys.version.split()[0])
               return
           elif self.flags['file']:
               print('filename = ' + self.flags['file'])
               return

           print('Program completed. Try adding "--help"')

   if __name__ == '__main__':
       cmd = Command(sys.argv[1:])
       if cmd.error:
           print('error: {0}'.format(cmd.error))
           sys.exit(1)
       else:
           sys.exit(cmd.run())


If we name this script ``example-comand`` and execute it, the following will be
the output for running ``example-command -h`` or ``example-command --help``::

   usage: example-command [options]

   An example of a basic CLI program

   Options:
   -h, --help                        show this help information
   -f <filename>, --file=<filename>  use specified file
   --version                         show version information


Contributing
============

You can use Bitbucket or Github for discussing code, reporting bugs and
sending pull-requests.

- Bitbucket: https://bitbucket.org/babab/pycommand
- Github: https://github.com/babab/pycommand


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
