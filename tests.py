# Copyright (c) 2013  Benjamin Althues <benjamin@babab.nl>
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

'''Tests:

>>> import pycommand
>>> import sys

>>> class BasicExampleCommand(pycommand.CommandBase):
...     usagestr = 'usage: basic-example [options]'
...     description = 'small description'
...     optionList = (
...         ('help', ('h', False, 'show this help information')),
...         ('file', ('f', '<filename>', 'use specified file')),
...         ('version', ('', False, 'show version information')),
...     )

>>> cmd1 = BasicExampleCommand(['-h'])
>>> cmd1.error
>>> print(cmd1.usage)
usage: basic-example [options]
<BLANKLINE>
small description
<BLANKLINE>
Options:
-h, --help                        show this help information
-f <filename>, --file=<filename>  use specified file
--version                         show version information
<BLANKLINE>
>>> cmd1.flags['help']
True
>>> cmd1.flags['file']
>>> cmd1.flags['version']

>>> cmd2 = BasicExampleCommand(['--file', '/path/to/a/filename', '--version'])
>>> cmd2.error
>>> cmd2.flags['help']
>>> cmd2.flags['file']
'/path/to/a/filename'
>>> cmd2.flags['version']
True

>>> cmd3 = BasicExampleCommand(['--doesnotexist', '-h', '-f', 'filename',
...                             '--version'])
>>> cmd3.error
GetoptError('option --doesnotexist not recognized', 'doesnotexist')
>>> cmd3.flags['help']
>>> cmd3.flags['file']
>>> cmd3.flags['version']
'''

if __name__ == '__main__':
    import doctest
    doctest.testmod()
