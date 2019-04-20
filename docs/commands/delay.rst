delay
=====

Synopsis
--------

``srcomp delay [-h] [--no-pull] [--verbose] [--skip-host-check] <compstate> <how_long> [when]``

Description
-----------

Add a delay to the scheduled timings.

This is a convenience wrapper around the ```add-delay`` <./add-delay>`__
and ```deploy`` <./deploy>`__ commands and is logically equivalent to
doing:

``srcomp add-delay <delay-args> && srcomp deploy <deploy-args>``
