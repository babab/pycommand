# Copyright (c) 2013-2015  Benjamin Althues <benjamin@babab.nl>
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

from nose.tools import (
    eq_,
    raises,
    timed,
)

import pycommand


class BasicTestCommand(pycommand.CommandBase):
    usagestr = 'usage: pycommand-test [options]'
    description = 'small description'
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('file', ('f', '<filename>', 'use specified file')),
        ('version', ('', False, 'show version information')),
    )


@timed(.005)
def test_args_empty():
    cmd = BasicTestCommand([])
    eq_(cmd.flags['help'], None)


@timed(.005)
def test_no_error():
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.error, None)


@timed(.005)
def test_flags_short_without_argument():
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags['help'], True)

    cmd = BasicTestCommand([''])
    eq_(cmd.flags['help'], None)


@timed(.005)
def test_flags_short_with_argument():
    cmd = BasicTestCommand(['-f', 'funny-cats.gif'])
    eq_(cmd.flags['file'], 'funny-cats.gif')

    cmd = BasicTestCommand([''])
    eq_(cmd.flags['file'], None)


@timed(.005)
def test_flags_mixed1():
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags['help'], True)
    eq_(cmd.flags['file'], None)
    eq_(cmd.flags['version'], None)


@timed(.005)
def test_flags_mixed2():
    cmd = BasicTestCommand(['-h', '--version'])
    eq_(cmd.flags['help'], True)
    eq_(cmd.flags['file'], None)
    eq_(cmd.flags['version'], True)


@timed(.005)
def test_flags_mixed3():
    cmd = BasicTestCommand(['-h', '--version', '--file', 'happy-puppies.gif'])
    eq_(cmd.flags['help'], True)
    eq_(cmd.flags['file'], 'happy-puppies.gif')
    eq_(cmd.flags['version'], True)


@timed(.005)
def test_flags_attributes():
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags.help, True)
    eq_(cmd.flags.file, None)
    eq_(cmd.flags.version, None)


@raises(pycommand.OptionError)
def test_flags_attribute_not_existing():
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags.tsixetonseod, None)
