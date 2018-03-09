'''A clean and simplistic alternative for argparse, optparse and getopt'''

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

from collections import OrderedDict
import getopt
import sys

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2013-2016, 2018  Benjamin Althues"
__version_info__ = (0, 3, 0, 'beta', 0)
__version__ = '0.3.0'


class CommandExit(Exception):
    def __init__(self, val):
        self.err = val

    def __str__(self):
        return repr(self.err)


class OptionError(AttributeError):
    '''Options/Flags AttributeError exception'''


class dictobject(dict):
    '''A dictionary with getters by attribute, used for flags '''
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise OptionError("Option '{}' is not defined".format(name))


class CommandBase(object):
    '''Base class for (sub)commands'''

    usagestr = 'usage: command [options]'
    '''String. Usage synopsis'''

    description = ''
    '''String. Small description of subcommand'''

    optionList = {}
    '''Dictionary of options (as a tuple of 2-tuples).
    This will be transformed to an OrderedDict when initializing the object.

    Example::

        optionList = (
            ('help', ('h', False, 'show this help information')),
            ('dry-run', ('n', False,
                         'only print output without actually running')),

            # To specify that an option requires an argument
            # just add a string that describes it
            ('file', ('f', '<filename>', 'use specified file')),

            # Use an empty string to ommit short option
            ('debug', ('', False, 'show debug information')),
        )

    '''

    usageTextExtra = ''
    '''String. Optional extra usage information'''

    commands = {}
    '''Dictionary of commands and the callables they invoke.'''

    def __init__(self, argv=sys.argv[1:]):
        '''Initialize (sub)command object

        :Parameters:
            - `argv`: List of arguments. E.g. `sys.argv[1:]`
        '''

        # Instance vars
        self.error = None
        '''Thrown by GetoptError when parsing illegal arguments.'''

        self.flags = {}
        '''Dict of parsed options and corresponding arguments, if any.'''

        self.args = []
        '''List of parsed postional arguments'''

        self.parentFlags = {}
        '''Dict of registered `flags` of parent Command object.'''

        self.usage = ''
        '''String with usage information

        The string is compiled using the values found for
        `usagestr`, `description`, `optionList` and `usageTextExtra`.
        '''

        self.optionList = OrderedDict(self.optionList)

        # Local vars
        longopts = []
        padding = 0
        shortopts = ''

        # Calculate padding needed for option arguments in usage info
        for flag, val in self.optionList.items():
            optlen = len(flag) + 2
            optlen += 4 if val[0] else 0
            optlen += len(val[1]) + 1 if val[0] and val[1] else 0
            optlen += len(val[1]) + 1 if val[1] else 0
            padding = optlen if optlen > padding else padding

        # Create usage information and build dict of possible flags
        opthelp = ''
        for flag, val in self.optionList.items():
            spec = flag + '=' if val[1] else flag
            longopts.append(spec)
            self.flags.update({flag: None})

            if val[1]:
                flagstring_long = ('{flag}={argument}'
                                   .format(flag=flag, argument=val[1]))
                if val[0]:
                    flagstring_short = ('{flag} {argument}'
                                        .format(flag=val[0], argument=val[1]))
            else:
                flagstring_long = flag
                flagstring_short = val[0]

            if val[0]:
                shortopts += val[0] + ':' if val[1] else val[0]
                optline = ('-{short}, --{flag}'
                           .format(short=flagstring_short,
                                   flag=flagstring_long))
            else:
                optline = '--{flag}'.format(flag=flagstring_long)

            opthelp += ('{options:{padding}}  {desc}\n'
                        .format(options=optline, padding=padding, desc=val[2]))

        self.usage = self.usagestr
        if self.description:
            self.usage += '\n\n{desc}'.format(desc=self.description)
        if self.optionList:
            self.usage += '\n\nOptions:\n{opts}'.format(opts=opthelp)
        if self.usageTextExtra:
            self.usage += '\n{help}'.format(help=self.usageTextExtra)

        # Parse arguments and options
        try:
            opts, self.args = getopt.getopt(argv, shortopts, longopts)
        except getopt.GetoptError as err:
            self.error = err
            return  # Stop when an invalid option is parsed

        for opt in opts:
            # Compare each option with optionList and set values for flags
            for flag, val in self.optionList.items():
                if opt[0][1] != '-':
                    # Short tags
                    if opt[0][1] == val[0]:
                        if val[1]:
                            self.flags[flag] = opt[1]
                        else:
                            self.flags[flag] = True
                else:
                    # Long tags
                    if opt[0][2:] == flag:
                        if val[1]:
                            self.flags[flag] = opt[1]
                        else:
                            self.flags[flag] = True

        # Convert to dictobject to allow getting flags by attribute name
        self.flags = dictobject(self.flags)

    def run(self):
        if not self.args:
            print(self.usage)
            raise CommandExit(2)
        elif self.args[0] in self.commands:
            return self.commands[self.args[0]](argv=self.args[1:])
        else:
            print('error: command {cmd} does not exist'
                  .format(cmd=self.args[0]))
            raise CommandExit(1)

    def registerParentFlag(self, optionName, value):
        '''Register a flag of a parent command

        :Parameters:
            - `optionName`: String. Name of option
            - `value`: Mixed. Value of parsed flag`
        '''
        self.parentFlags.update({optionName: value})
        return self


def run_and_exit(command_class):
    '''A shortcut for reading from sys.argv and exiting the interpreter'''
    cmd = command_class(sys.argv[1:])
    if cmd.error:
        print('error: {0}'.format(cmd.error))
        sys.exit(1)
    else:
        sys.exit(cmd.run())


if __name__ == '__main__':
    # What follows is the pycommand generator script, with embedded templates.
    # This can be run by executing the module directly (python -m pycommand)
    import os
    import stat
    import string

    try:
        input = raw_input
    except NameError:
        pass

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

    class PycommandGenerator(CommandBase):
        '''Generate a shell command from a template'''

        usagestr = 'usage: python -m pycommand [options]'
        description = __doc__
        optionList = (
            ('generate', ('g', False, 'generate a shell command')),
            ('help', ('h', False, 'show this help information')),
            ('version', ('v', False, 'show version information')),
        )

        variables = {
            'name': 'mycommand',
            'classname': 'Command',
        }
        template = ''

        def run(self):
            if self.flags['version']:
                print('pycommand version ' + __version__)
                return 0
            elif self.flags['generate']:
                print('pycommand v{} - script generator'.format(__version__))
                self.askVar('name', 'name of executable')
                self.askVar('classname', 'name of class')
                self.askTemplate()
                return 0 if self.save() else 1
            else:
                print(self.usage)
                return 0

        def askVar(self, varName, question):
            inp = input(question + ' [{}]: '.format(self.variables[varName]))
            self.variables[varName] = inp if inp else self.variables[varName]

        def askTemplate(self):
            inp = 0
            while inp not in range(1, 3):
                print('select a template:')
                print(' 1 - basic')
                print(' 2 - basic (without explaining comments)')
                try:
                    inp = int(input('Enter a number [1-2]: '))
                except ValueError:
                    inp = 0

            inp = str(inp)
            if inp == '1':
                self.template = string.Template(
                    templates['basic-with-comments']
                )
            elif inp == '2':
                self.template = string.Template(templates['basic-no-comments'])
            else:
                raise Exception('Invalid template choice')

        def save(self):
            basepath = os.path.abspath(os.path.curdir)
            dumpfile = basepath + '/' + self.variables['name']

            if os.path.isfile(dumpfile):
                print('File "' + dumpfile + '" already exists.')
                print('Using "/tmp/' + self.variables['name'] + '"')
                dumpfile = '/tmp/' + self.variables['name']

            try:
                with open(dumpfile, 'w') as dump:
                    dump.write(self.template.substitute(self.variables))
            except OSError:
                print('Error writing to file "' + dumpfile + '"')
                return False

            os.chmod(
                dumpfile,
                os.stat(dumpfile).st_mode |
                stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            )
            print('Written to "' + dumpfile + '"')
            print('Try running it with "' + dumpfile + ' --help"')
            return True

    # Run pycommand generator
    try:
        run_and_exit(PycommandGenerator)
    except KeyboardInterrupt:
        print('')
