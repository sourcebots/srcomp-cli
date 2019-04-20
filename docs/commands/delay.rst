delay
=====

Synopsis
--------

``srcomp delay [-h] [--no-pull] [--verbose] [--skip-host-check] <compstate> <how_long> [when]``

Description
-----------

Add a delay to the scheduled timings.

This is a convenience wrapper around the |add-delay|_ and |deploy|_ commands and
is logically equivalent to doing:

``srcomp add-delay <delay-args> && srcomp deploy <deploy-args>``


.. |add-delay| replace:: ``add-delay``
.. _add-delay: ./add-delay.html

.. |deploy| replace:: ``deploy``
.. _deploy: ./deploy.html
