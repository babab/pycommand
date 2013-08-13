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
   # cd pycommand
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

           After the object has been created, there are 4 instance
           variables ready for you to use to write the flow of the program.
           In this example we only use the following three::

               error -- Thrown by GetoptError when parsing illegal
                        arguments

               flags -- OrderedDict of parsed options and corresponding
                        arguments, if any.

               usage -- String with usage information. The string
                        is compiled using the values found for `usagestr`,
                        `description`, `optionList` and `usageTextExtra`.

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

Here is a full example demonstrating essentially the same program, but
with the ``--help`` and ``--version`` options replaced for subcommands::

   #!/usr/bin/env python

   import pycommand
   import sys


   class FullExampleCommand(pycommand.CommandBase):
       '''An full example of a pycommand CLI program

       This is an example that demonstrates the mapping of postional
       arguments to subcommands, registrering the --file flag from the main
       command to its subcommand. It only explains new concepts that are
       not handled in ``basic-example``, so be sure to see that first.

       '''
       usagestr = 'usage: full-example [-f <filename>] <command> [<args>]'
       description = (
           'Commands:\n'
           '   help         show this help information\n'
           '   version      show full version information'
       )
       optionList = (('file', ('f', '<filename>', 'use specified file')), )

       # Optional extra usage information
       usageTextExtra = (
           "See 'full-example help <command>' for more information on a "
           "specific command."
       )

       def run(self):
           '''The `run` method of the main command

           After the object has been created, there are 4 instance
           variables ready for you to use to write the flow of the program.
           In this example we use them all::

               error -- Thrown by GetoptError when parsing illegal
                        arguments

               flags -- OrderedDict of parsed options and corresponding
                        arguments, if any.

               usage -- String with usage information. The string
                        is compiled using the values found for `usagestr`,
                        `description`, `optionList` and `usageTextExtra`.

               parentFlags -- Dict of registered `flags` of another
                              `CommandBase` object.

           '''
           if not self.args:
               print(self.usage)
               return 2
           elif self.args[0][0] == 'h':
               cmd = HelpCommand(argv=self.args[1:])
           elif self.args[0][0] == 'v':
               cmd = VersionCommand(argv=self.args[1:])
           else:
               print('error: command {cmd} does not exist'
                     .format(cmd=self.args[0]))
               return 1

           # Register a flag of a parent command

           # :Parameters:
           #     - `optionName`: String. Name of option
           #     - `value`: Mixed. Value of parsed flag`
           cmd.registerParentFlag('file', self.flags['file'])

           if cmd.error:
               print('full-example {cmd}: {error}'
                     .format(cmd=self.args[0], error=cmd.error))
               return 1
           else:
               return cmd.run()


   class HelpCommand(pycommand.CommandBase):
       usagestr = 'usage: full-example help [<command>]'
       description = 'Show help information'

       def run(self):
           if not self.args or self.args[0][0] == 'h':
               print(FullExampleCommand([]).usage)
               return
           elif self.args[0][0] == 'v':
               print(VersionCommand([]).usage)
               return
           else:
               print('error: command {cmd} does not exist'
                     .format(cmd=self.args[0]))
               return 1
           print(cmd.usage)


   class VersionCommand(pycommand.CommandBase):
       usagestr = 'usage: full-example version'
       description = 'Show version information'

       def run(self):
           print('Python version ' + sys.version.split()[0])
           print('Fileflag = {0}'.format(self.parentFlags['file']))


   if __name__ == '__main__':
       cmd = FullExampleCommand(sys.argv[1:])
       if cmd.error:
           print('error: {0}'.format(cmd.error))
           sys.exit(1)
       else:
           sys.exit(cmd.run())


And here are some outputs::

   $ ./full-example
   usage: full-example [-f <filename>] <command> [<args>]

   Commands:
      help         show this help information
      version      show full version information

   Options:
   -f <filename>, --file=<filename>  use specified file

   See 'full-example help <command>' for more information on a specific command.

   $ ./full-example help version
   usage: full-example version

   Show version information

   $ ./full-example -f
   error: option -f requires argument

   $ ./full-example -f somefilename version
   Python version 3.3.2
   Fileflag = somefilename

   $ ./full-example version
   Python version 3.3.2
   Fileflag = None

   $ ./full-example h doesnotexist
   error: command doesnotexist does not exist


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