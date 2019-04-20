delay
=====

Synopsis
--------

``srcomp delay [-h] [--no-pull] [--verbose] [--skip-host-check] <compstate> <how_long> [when]``

Description
-----------

Add a delay to the scheduled timings.

This is a convenience wrapper around the |add-delay|_, |validate|_ and |deploy|_
commands and is roughly equivalent to doing:

.. code::

    $ (cd path/to/compstate \
        && srcomp add-delay . 90s \
        && srcomp validate . \
        && git commit schedule.yaml --message "Adding 90s delay at $(date)"
        && srcomp deploy .)

.. |add-delay| replace:: ``add-delay``
.. _add-delay: ./add-delay.html

.. |validate| replace:: ``validate``
.. _validate: ./validate.html

.. |deploy| replace:: ``deploy``
.. _deploy: ./deploy.html
