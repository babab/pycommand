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

from nose.tools import (
    eq_,
    raises,
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


def test_args_empty():
    '''Flags should be None by default'''
    cmd = BasicTestCommand([])
    eq_(cmd.flags['help'], None)


def test_no_error():
    '''cmd.error should be None by default'''
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.error, None)


def test_flags_short_without_argument():
    '''When a flag is given, it's value should be True, else None'''
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags['help'], True)

    cmd = BasicTestCommand([''])
    eq_(cmd.flags['help'], None)


def test_flags_short_with_argument():
    '''If flags take arguments that should become the value, else None'''
    cmd = BasicTestCommand(['-f', 'funny-cats.gif'])
    eq_(cmd.flags['file'], 'funny-cats.gif')

    cmd = BasicTestCommand([''])
    eq_(cmd.flags['file'], None)


def test_flags_mixed1():
    '''Test True/None status of defined flags with 1 argument'''
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags['help'], True)
    eq_(cmd.flags['file'], None)
    eq_(cmd.flags['version'], None)


def test_flags_mixed2():
    '''Test True/None status of defined flags with 2 arguments'''
    cmd = BasicTestCommand(['-h', '--version'])
    eq_(cmd.flags['help'], True)
    eq_(cmd.flags['file'], None)
    eq_(cmd.flags['version'], True)


def test_flags_mixed3():
    '''Test True/None status of defined flags with 3 arguments'''
    cmd = BasicTestCommand(['-h', '--version', '--file', 'happy-puppies.gif'])
    eq_(cmd.flags['help'], True)
    eq_(cmd.flags['file'], 'happy-puppies.gif')
    eq_(cmd.flags['version'], True)


def test_flags_attributes():
    '''Flags should be accessible by attribute'''
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags.help, True)
    eq_(cmd.flags.file, None)
    eq_(cmd.flags.version, None)


@raises(pycommand.OptionError)
def test_flags_attribute_not_existing():
    '''Accessing unset attributes raises an OptionError'''
    cmd = BasicTestCommand(['-h'])
    eq_(cmd.flags.tsixetonseod, None)
