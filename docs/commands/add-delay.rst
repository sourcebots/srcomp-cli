add-delay
=========

Synopsis
--------

``srcomp srcomp add-delay [-h] <compstate> <how_long> [when]``

Description
-----------

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

The time at which the delay applies can be specified as a human-readable string
either of an absolute time, such as ``2019-04-06 12:00``, or as a relative time,
such as ``now`` or ``now + 5 minutes``.

Alternatively, you can specify ``current match`` in order to have the delay
inserted at the start of the current match slot.

.. note:: Parsed times are always interpretted in the local system timezone,
          rather than the compstate's configured timezone.
