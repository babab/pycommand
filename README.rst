pycommand
******************************************************************************

Create (recursive trees of) executable commands using minimal code.

pycommand is a module with one simple `CommandBase` class
that you can use to create executable commands for your python programs with
very simplistic and readable code.

Here is a typical example of a very common idiom when building command line
interfaces, by writing a class that overrides `pycommand.CommandBase`::

   #!/usr/bin/env python

   import pycommand


   class CommandExample(pycommand.CommandBase):
       usagestr = 'usage: commandname [options]'
       description = 'This is a description'
       optionList = (
           ('help', ('h', False, 'show this help information')),
           ('version', ('V', False, 'show version information')),
       )
       usageTextExtra = 'This is extra usage info'

       def run(self):
           if self.flags['help']:
               print(self.usage)
               return
           elif self.flags['version']:
               print('Python version ' + sys.version.split()[0])
               return

   if __name__ == '__main__':
       import sys
       cmd = CommandExample(sys.argv[1:])
       sys.exit(cmd.run())


And here is the output for running
``commandname -h`` or ``commandname --help``::

   usage: commandname [options]

   This is a description

   Options:
   -h, --help     show this help information
   -V, --version  show version information

   This is extra usage info

The ``description``, ``optionList`` and ``usageTextExtra`` properties are
optional. More info and examples soon.


Download and install
====================

::
   $ git clone git://bitbucket.org/babab/pycommand.git
   # python setup.py install


Software license
==============================================================================

Copyright (c) 2013  Benjamin Althues <benjamin@babab.nl>

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
