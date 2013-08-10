pycommand
******************************************************************************

.. toctree::
   :maxdepth: 2

**Parse command line arguments / define (sub)commands with minimal code**

Pycommand consists of one simple `CommandBase` class that you can use to
create executable commands for your python programs with very simplistic
and readable code. It has support for nesting commands, so you can
create (multiple levels of) subcommands, with the ability to pass the
values of optional arguments of a command object to its subcommand
objects. Supported Python versions are 2.7 and 3.3

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
   # python setup.py install


Example #1 - A Basic command
============================

Here is a typical example of a very common command line interface program::

   #!/usr/bin/env python

   import pycommand
   import sys


   class BasicExampleCommand(pycommand.CommandBase):
       '''An example of a basic CLI program

       This is an example that demonstrates the handling of all possible
       settings for the optional arguments, managed via the `optionList`.
       This example does not handle positional arguments.

       '''
       usagestr = 'usage: basic-example [options]'
       description = __doc__.split('\n')[0]

       # optionList is a tuple of 2-tuples, in format:
       # (long-option, (short-option, argument, help-information))
       #
       # The order in which you define the options will be the order
       # in which they will appear in the usage message
       optionList = (
           ('help', ('h', False, 'show this help information')),

           # To specify that an option requires an argument just add a
           # string that describes it
           ('file', ('f', '<filename>', 'use specified file')),

           # Use an empty string to ommit short option. Long option names
           # cannot be ommitted, since they are used as dictionary keys in
           # `self.flags` which holds the validated input
           ('version', ('', False, 'show version information')),
       )

       def run(self):
           '''The `run` method of the main command

           You need to define a method in your class that actually deals
           with any options that the user of your program has set. We call
           it `run` here, but you can name it whatever you want.

           After the object has been created, there are 5 instance
           variables ready for you to use to write the flow of the program.
           In this example we only use the following three::

               self.error -- Thrown by GetoptError when parsing illegal
                             arguments

               self.flags -- OrderedDict of parsed options and corresponding
                             arguments, if any.

               self.usage -- String with usage information. The string
                             is compiled using the values found for
                             `usagestr`, `description`, `optionList` and
                             `usageTextExtra`.

           '''
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
       cmd = BasicExampleCommand(sys.argv[1:])
       if cmd.error:
           print('error: {0}'.format(cmd.error))
           sys.exit(1)
       else:
           sys.exit(cmd.run())


If we name this script ``basic-example`` and execute it, the following will be
the output for running ``basic-example -h`` or ``basic-example --help``::

   usage: basic-example [options]

   An example of a basic CLI program

   Options:
   -h, --help                        show this help information
   -f <filename>, --file=<filename>  use specified file
   --version                         show version information


Example #2 - Full example of one main command with two subcommands
==================================================================

TODO


Module documentation
====================

.. automodule:: pycommand
   :members:


Contributing
============

You can use Bitbucket or Github for discussing code, reporting bugs and
sending pull-requests.

- Bitbucket: https://bitbucket.org/babab/pycommand
- Github: https://github.com/babab/pycommand


Software license
================

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
