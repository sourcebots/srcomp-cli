Student Robotics Competition Command Line Interface
===================================================

SRComp CLI is a set of command-line tools for operating SRComp at a competition
and for working with compstate repositories.

Installation
------------

You can install SRComp CLI using ``pip``:

.. code:: shell

    pip install git+https://github.com/PeterJCLaw/srcomp git+https://github.com/PeterJCLaw/srcomp-cli

Bash completions are also available, see the ``bash-completion`` file in the
root of the repo.

Commands
--------

All the tools are provided as sub-commands to the primary `srcomp` program. As
there are more commands than are fully documented here, you are encouraged to
run ``srcomp --help`` to get information about the commands.

.. toctree::
   :glob:
   :maxdepth: 1

   commands/*

API
---

SRComp CLI does not have a Python API as such, however its `shared internals
<./api.html>`_ are documented as a guide for developers adding new commands.

.. toctree::
   :hidden:

   api
