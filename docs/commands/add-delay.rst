add-delay
=========

Add a delay to the scheduled timings.

The match schedule supports having delays added in order to cope with delays to
the planned schedule. Delays will affect any matches which were scheduled
automatically within match periods, such as league matches and knockout matches
when using the automatic scheduler, and whose match slot is scheduled to start
at or after the time at which the delay occurs.

.. note:: Tiebreaker matches and knockout matches scheduled by the static
          scheduler are not affected by delays.

The duration of the delay should be specified in the format ``1hr2m3s``, each
granularity of which is optional. For example, specifications such as ``2hr3s``
or ``5m`` are valid.

The time at which the delay applies can be specified in a number of formats:

 * ``now`` (default)
 * ``current match`` -- the start of the current match slot
 * ``<duration> ago`` or ``in <duration>``, using the same duration spelling as
   for the length of the delay (see above)
 * an absolute time, such as ``2019-04-06 12:00``, which will be parsed by ``dateutil``

.. note:: Parsed times are always interpreted in the local system timezone,
          rather than the compstate's configured timezone.

Command Help
------------

.. argparse::
   :module: sr.comp.cli.command_line
   :func: argument_parser
   :prog: srcomp
   :path: add-delay
