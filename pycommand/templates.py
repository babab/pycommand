# Copyright (c) 2013-2016, 2018  Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

templates = {}
templates['basic-with-comments'] = """#!/usr/bin/env python

import pycommand


class $classname(pycommand.CommandBase):
    '''description of the program, used below as __doc__'''
    usagestr = 'usage: $name [options]'
    description = __doc__

    # optionList is a tuple of 2-tuples, in format:
    # (long-option, (short-option, argument, help-information))
    #
    # The order in which you define the options will be the order
    # in which they will appear in the usage message
    optionList = (
        ('help', ('h', False, 'show this help information')),

        # To specify that an option requires an argument just add a
        # string that describes it

        # ('file', ('f', '<filename>', 'use specified file')),

        # Use an empty string to ommit short option. Long option names
        # cannot be ommitted, since they are used as dictionary keys in
        # `self.flags` which holds the validated input

        # ('version', ('', False, 'show version information')),
    )

    def run(self):
        '''The `run` method of the $name command

        You need to define a method in $classname that actually deals
        with any options that the user of your program has set. We call
        it `run` here, but you can name it whatever you want.

        After the object has been created, there are 4 instance
        variables ready for you to use to write the flow of the program.
        In this example we only use the following three::

            error -- Thrown by GetoptError when parsing illegal
                     arguments

            flags -- Object/dict of parsed options and corresponding
                     arguments, if any.

            usage -- String with usage information. The string
                     is compiled using the values found for `usagestr`,
                     `description`, `optionList` and `usageTextExtra`.

        '''
        if self.flags.help:
            print(self.usage)
            return 0
        # elif self.flags.version:
        #     print('Python version ' + sys.version.split()[0])
        #     return 0
        # elif self.flags.file:
        #     print('filename = ' + self.flags.file)
        #     return 0

        print('Program completed. Try adding "--help"')

if __name__ == '__main__':
    # Shortcut for reading from sys.argv[1:] and sys.exit(status)
    pycommand.run_and_exit($classname)

    # The shortcut is equivalent to the following:

    # cmd = $classname(sys.argv[1:])
    # if cmd.error:
    #     print('error: {0}'.format(cmd.error))
    #     sys.exit(1)
    # else:
    #     sys.exit(cmd.run())
"""

templates['basic-no-comments'] = """#!/usr/bin/env python

import pycommand


class $classname(pycommand.CommandBase):
    '''description of the program, used below as __doc__'''
    usagestr = 'usage: $name [options]'
    description = __doc__
    optionList = (
        ('help', ('h', False, 'show this help information')),
        # ('file', ('f', '<filename>', 'use specified file')),
        # ('version', ('', False, 'show version information')),
    )

    def run(self):
        if self.flags.help:
            print(self.usage)
            return 0
        # elif self.flags.version:
        #     print('Python version ' + sys.version.split()[0])
        #     return 0
        # elif self.flags.file:
        #     print('filename = ' + self.flags.file)
        #     return 0

        print('Program completed. Try adding "--help"')

if __name__ == '__main__':
    pycommand.run_and_exit($classname)
"""
templates['full-with-comments'] = r"""#!/usr/bin/env python

import pycommand
import sys


class VersionCommand(pycommand.CommandBase):
    usagestr = 'usage: $name version'
    description = 'Show version information'

    def run(self):
        print('Python version ' + sys.version.split()[0])
        print('Fileflag = {0}'.format(self.parentFlags['file']))


class HelpCommand(pycommand.CommandBase):
    usagestr = 'usage: $name help [<command>]'
    description = 'Show help information'

    def run(self):
        if self.args:
            if self.args[0] == 'help':
                print(self.usage)
                print('Fileflag = {0}'.format(self.parentFlags['file']))
            elif self.args[0] == 'version':
                print(VersionCommand([]).usage)
        else:
            print($classname([]).usage)


class $classname(pycommand.CommandBase):
    '''An full example of a pycommand CLI program

    This is an example that demonstrates the mapping of subcommands
    and registrering the --file flag from the main command to its
    subcommands. It only explains new concepts that are not handled in
    ``basic-example``, so be sure to see that first.

    '''
    usagestr = 'usage: $name [-f <filename>] <command> [<args>]'
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
        "See '$name help <command>' for more information on a "
        "specific command."
    )

    def run(self):
        '''The `run` method of the main command

        After the object has been created, there are 4 instance
        variables ready for you to use to write the flow of the program.
        In this example we use them all::

            error -- Thrown by GetoptError when parsing illegal
                     arguments

            flags -- Object/dict of parsed options and corresponding
                     arguments, if any.

            usage -- String with usage information. The string
                     is compiled using the values found for `usagestr`,
                     `description`, `optionList` and `usageTextExtra`.

            parentFlags -- Dict of registered `flags` of another
                           `CommandBase` object.

        '''
        try:
            cmd = super($classname, self).run()
        except pycommand.CommandExit as e:
            return e.err

        # Register a flag of a parent command
        # :Parameters:
        #     - `optionName`: String. Name of option
        #     - `value`: Mixed. Value of parsed flag`
        cmd.registerParentFlag('file', self.flags.file)

        if cmd.error:
            print('$name {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()


if __name__ == '__main__':
    # Shortcut for reading from sys.argv[1:] and sys.exit(status)
    pycommand.run_and_exit($classname)
"""
templates['full-no-comments'] = r"""#!/usr/bin/env python

import pycommand
import sys


class VersionCommand(pycommand.CommandBase):
    usagestr = 'usage: $name version'
    description = 'Show version information'

    def run(self):
        print('Python version ' + sys.version.split()[0])
        print('Fileflag = {0}'.format(self.parentFlags['file']))


class HelpCommand(pycommand.CommandBase):
    usagestr = 'usage: $name help [<command>]'
    description = 'Show help information'

    def run(self):
        if self.args:
            if self.args[0] == 'help':
                print(self.usage)
                print('Fileflag = {0}'.format(self.parentFlags['file']))
            elif self.args[0] == 'version':
                print(VersionCommand([]).usage)
        else:
            print($classname([]).usage)


class $classname(pycommand.CommandBase):
    usagestr = 'usage: $name [-f <filename>] <command> [<args>]'
    description = (
        'Commands:\n'
        '   help         show this help information\n'
        '   version      show full version information'
    )

    commands = {'help': HelpCommand,
                'version': VersionCommand}
    optionList = (('file', ('f', '<filename>', 'use specified file')), )
    usageTextExtra = (
        "See '$name help <command>' for more information on a "
        "specific command."
    )

    def run(self):
        try:
            cmd = super($classname, self).run()
        except pycommand.CommandExit as e:
            return e.err

        cmd.registerParentFlag('file', self.flags.file)
        if cmd.error:
            print('$name {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()


if __name__ == '__main__':
    pycommand.run_and_exit($classname)
"""
