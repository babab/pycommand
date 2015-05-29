Change Log
==========

pycommand adheres to `Semantic Versioning <http://semver.org/>`_.


0.3.0 - Development version - UNRELEASED
----------------------------------------

Added
#####
- Shortcut ``run_and_exit()`` for reading from ``sys.argv[1:]`` and exiting
  the interpreter via ``sys.exit(status)``
- Package as (source and) wheel distribution to speed up installations
- Install ``man`` page in ``/usr/share/man3/``


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
