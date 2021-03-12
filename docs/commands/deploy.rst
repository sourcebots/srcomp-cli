deploy
======

Synopsis
--------

``srcomp deploy [-h] [--verbose] [--skip-host-check] compstate``

Description
-----------

Deploy the compstate to its various deployments.

This is the canonical way to push a local compstate onto host machines;
specifically it will target those specified in the ``deployments.yaml``
file within the compstate.

Compstates must not have local changes or untracked files (as reported
by ``git status``) and must be valid in order to be deployed.

During deployment, the states of the hosts relative to the current state
are checked and the user will be warned if:

-  the state of a host was unavailable (for example due to network
   errors)
-  the state of a host appears to be more recent than the current state
   (as determined by git ancestry)
-  the state of a host appears to be unrelated to the current state
   (again as determined by git ancestry)

In any case, the user is able to continue with the deployment
interactively.

The ``deployments.yaml`` file contains a list of fully qualified names
of machines which have deployments which support triggered updates. An
example file might look like this:

.. code:: yaml

    deployments:
      - srcomp.studentrobotics.org
      - compbox.local

Host are tried in the order specified in the ``deployments.yaml`` file
and failures in deploying to any host *do not* prevent deployment to
later hosts.

Each host is assumed to:

-  be running a copy of |srcomp-http|_ at ``/comp-api``, from which its current
   state can be queried
-  have a local user ``srcomp`` which has:

   -  key-based SSH access enabled using a key available to the user
      running the command
   -  a ``compstate.git`` in its home directory
   -  an executable file ``update`` in its home directory which accepts
      as single argument the revision being deployed and subsequently
      calls the function ``sr.comp.http.update.main()`` with the path to
      the live compstate and that revision as the proper ``sys.argv`` values.

The usual way to achieve this is to configure a host using |srcomp-puppet|_,
which contains the canonical implementation.

.. |srcomp-http| replace:: ``srcomp-http``
.. _srcomp-http: https://github.com/PeterJCLaw/srcomp-http

.. |srcomp-puppet| replace:: ``srcomp-puppet``
.. _srcomp-puppet: https://github.com/PeterJCLaw/srcomp-puppet
