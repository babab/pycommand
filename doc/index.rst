pycommand 0.3.0-dev
******************************************************************************

.. image:: https://travis-ci.org/babab/pycommand.svg?branch=master
    :target: https://travis-ci.org/babab/pycommand

.. toctree::
   :maxdepth: 2

**A clean and simplistic alternative for argparse, optparse and getopt**

Pycommand is essentially a fancy wrapper around getopt that consists of
one simple `CommandBase` class that you can use to create executable
commands for your python programs with very simplistic and readable
code. It has support for subcommands and also nesting commands, so you
can create (multiple levels of) subcommands, with the ability to pass
the values of optional arguments of a command object to its subcommand
objects. Supported Python versions are 2.7 and 3.2 and later.


Download and install
====================

If you have pip installed, you can just:

.. code-block:: console

   # pip install pycommand

To work with the current development version, do something like this:

.. code-block:: console

   $ git clone git://bitbucket.org/babab/pycommand.git
   # cd pycommand
   # python setup.py install


Quick setup from a template
===========================

To quicly start writing a command from a template (much like the
examples below), use pycommand's helper script by running:

.. code-block:: console

   $ pycommand init

This will ask you for an executable name, class name and template type
and it will save it to an executable file, ready to be used as a Python
shell script (for your Python package/module)).


Example #1 - A Basic command
============================

Here is a demonstration of the automated usage text generation and
parsing of optional arguments.

If we name the script for which you can see the code below
``basic-example`` and execute it, the following will be the output for
running ``basic-example -h`` or ``basic-example --help``:

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
       # Shortcut for reading from sys.argv[1:] and sys.exit(status)
       pycommand.run_and_exit(BasicExampleCommand)


Example #2 - Full example of one main command with two subcommands
==================================================================

Here is a full example demonstrating essentially the same program, but
with the ``--help`` and ``--version`` options replaced for subcommands:

.. code-block:: python

   #!/usr/bin/env python

   import pycommand
   import sys


   class VersionCommand(pycommand.CommandBase):
       usagestr = 'usage: full-example version'
       description = 'Show version information'

       def run(self):
           print('Python version ' + sys.version.split()[0])
           print('Fileflag = {0}'.format(self.parentFlags['file']))


   class HelpCommand(pycommand.CommandBase):
       usagestr = 'usage: full-example help [<command>]'
       description = 'Show help information'

       def run(self):
           if self.args and self.args[0] == 'version':
               print(VersionCommand([]).usage)
           print(cmd.usage)


   class FullExampleCommand(pycommand.CommandBase):
       '''An full example of a pycommand CLI program

       This is an example that demonstrates the mapping of subcommands
       and registrering the --file flag from the main command to its
       subcommand. It only explains new concepts that are not handled in
       ``basic-example``, so be sure to see that first.

       '''
       usagestr = 'usage: full-example [-f <filename>] <command> [<args>]'
       description = (
           'Commands:\n'
           '   help         show this help information\n'
           '   version      show full version information'
       )

       # Mapping of subcommands
       commands = {'help': HelpCommand,
                   'version': VersionCommand}

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
           try:
               cmd = super(FullExampleCommand, self).run()
           except pycommand.CommandExit as e:
               return e.err

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


   if __name__ == '__main__':
       # Shortcut for reading from sys.argv[1:] and sys.exit(status)
       pycommand.run_and_exit(FullExampleCommand)


And here are some output examples:

.. code-block:: console

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

   $ ./full-example help doesnotexist
   error: command doesnotexist does not exist


Module documentation
====================

.. automodule:: pycommand
   :members:


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


Contributing
============

You can use Bitbucket or Github for discussing code, reporting bugs and
sending pull-requests.

- Bitbucket: https://bitbucket.org/babab/pycommand
- Github: https://github.com/babab/pycommand


.. include:: ../CHANGELOG.rst


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
