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

from __future__ import absolute_import

'''
pycommand shell command and generator script.

This can be run by executing the __main__ module (python -m pycommand).
'''

import os
import stat
import string

from pycommand import (
    CommandBase,
    CommandExit,
    __version__,
)
from pycommand.templates import templates

try:
    input = raw_input
except NameError:
    pass


class PycommandGenerator(CommandBase):
    '''Generate a shell command from a template'''

    usagestr = 'usage: python -m pycommand init [options]'
    description = __doc__
    optionList = (
        ('template', ('t', '<number>', 'use template number')),
        ('help', ('h', False, 'show this help information')),
    )

    variables = {
        'name': 'mycommand',
        'classname': 'Command',
    }
    template = ''

    def run(self):
        if self.flags.help:
            print(self.usage)
            return 0

        print('pycommand v{} - script generator'.format(__version__))
        if self.flags.template:
            if int(self.flags.template) not in range(1, 5):
                print('error: template "{}" does not exist'
                      .format(self.flags.template))
                return 1
            self.setTemplate(self.flags.template)
        else:
            self.setTemplate(self.askTemplate())
        self.askVar('name', 'name of executable')
        self.askVar('classname', 'name of class')
        return 0 if self.save() else 1

    def setTemplate(self, template_n):
        template_n = str(template_n)
        if template_n == '1':
            self.template = string.Template(
                templates['basic-with-comments']
            )
        elif template_n == '2':
            self.template = string.Template(templates['basic-no-comments'])
        elif template_n == '3':
            self.template = string.Template(
                templates['full-with-comments']
            )
        elif template_n == '4':
            self.template = string.Template(templates['full-no-comments'])
        else:
            raise Exception('Invalid template choice')

    def askVar(self, varName, question):
        inp = input(question + ' [{}]: '.format(self.variables[varName]))
        self.variables[varName] = inp if inp else self.variables[varName]

    def askTemplate(self):
        inp = 0
        while inp not in range(1, 5):
            print('''
Basic template:
* supports --options and argument parsing
* suitable for most use cases

Full template (uses objects for its subcommands):
* subcommands can have their own --options and subcommands parsing
* subcommands can have subcommands that can have subcommands
* access values for --some-option from a parent command in its child command.
''')
            print('select a template:')
            print(' 1 - basic')
            print(' 2 - basic (without explaining comments)')
            print(' 3 - full with subcommand objects')
            print(' 4 - full with subcommand objects (without comments)')
            try:
                inp = int(input('Enter a number [1-4]: '))
            except ValueError:
                inp = 0
        return inp

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


class PycommandShellMain(CommandBase):
    usagestr = 'usage: python -m pycommand [options] <command>'
    description = (
        'Commands:\n  init - Generate a shell command from a template'
    )

    commands = {'init': PycommandGenerator}
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('version', ('v', False, 'show version information')),
    )
    usageTextExtra = (
        "See 'python -m pycommand --help' for more information"
    )

    def run(self):
        # Handle --version and --help
        if self.flags.version:
            print('pycommand version ' + __version__)
            return 0
        elif self.flags.help:
            print(self.usage)
            return 0
        # Handle subcommands
        try:
            cmd = super(PycommandShellMain, self).run()
        except CommandExit as e:
            return e.err
        # Handle errors
        if cmd.error:
            print('python -m pycommand {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()
