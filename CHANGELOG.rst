Change Log
==========

pycommand adheres to `Semantic Versioning <http://semver.org/>`_.

0.4.0 - 2018-03-27
------------------

Added
#####
- Full templates can now (also) be auto generated
- CI testing for Python 3.5 and 3.6

Changed
#######

.. note::

   The ``pycommand init`` script is removed and is included in the
   pycommand package itself.

   To auto generate scripts from templates, from now on use:

      python -m pycommand init


- The code is split up into several modules and pycommand is now
  distributed as a package rather than a single module. The public
  API does not change however, all relevant members (CommandBase,
  run_and_exit) that are now placed in pycommand.pycommand are
  exposed through __init__ and therefore are still available as
  ``pycommand.CommandBase`` and ``pycommand.run_and_exit``.
- Code generator is included in the package itself instead of
  using an installed script (``pycommand init``)
- All templates are now embedded as well

Removed
#######
- Pycommand init script (installed into /usr/local/bin)
- Templates directory
- GNU info docs and manpage from distribution (they can still be generated)

  * pycommand.3 (prev. installed into /share/man/man3)
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
