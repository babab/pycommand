Change Log
==========

pycommand adheres to `Semantic Versioning <http://semver.org/>`_.

Git version (next release)
----------------------------

.. note::

   The ``pycommand init`` script is removed and is embedded in the
   pycommand module itself.

   To auto generate scripts from templates from now on, use:

      python -m pycommand -g


Added
#####
- Full templates can now (also) be auto generated
- CI testing for Python 3.5 and 3.6

Changed
#######
- Code generator is embedded in the pycommand module itself instead of
  using an installed script (``pycommand init``)
- All templates are now embedded as well

Removed
#######
- Pycommand init script (installed into /usr/local/bin)
- Templates directory
- GNU info docs and manpage from distribution (they can still be generated)

  * pycommand.3 (installed into /share/man/man3
  * pycommand.info


0.3.0 - 2015-06-04
------------------

Added
#####
- Shortcut ``run_and_exit()`` for reading from ``sys.argv[1:]`` and exiting
  the interpreter via ``sys.exit(status)``
- Package as wheel distribution to speed up installations
- Add ``man pycommand`` ability, i.e. install mandoc in ``/usr/share/man3/``

Changed
#######
- Add support for getting flags by attribute like ``self.flags.help``.
  The default approach for normal dicts like ``self.flags['help']``
  remains valid.


0.2.0 - 2015-05-21
------------------

Added
#####
- Full example of a command with subcommands
- Create quick templates via pycommand script (``pycommand init``)
- Unit tests and automatic testing via Travis-CI
- Documentation ``man`` (.3) and ``info`` (.info) pages

Changed
#######
- Specification of subcommands can be `defined in CommandBase.command`__
  as a shortcut.

__ https://github.com/babab/pycommand/commit/a978a05ef92f70f0ce6b06d96a38c2caa8297ecc

0.1.0 - 2013-08-08
------------------
Added
#####
- Initial release
