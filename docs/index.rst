Student Robotics Competition Command Line Interface
===================================================

SRComp CLI is a set of command-line tools for operating SRComp at a competition
and for working with compstate repositories.

Installation
------------

You can install SRComp CLI using ``pip``:

.. code:: shell

    pip install -U pip setuptools wheel
    pip install sr.comp.cli

Bash completions are also available, see the ``bash-completion`` file in the
root of the repo.

Commands
--------

The CLI tools are provided as sub-commands of a single ``srcomp`` program:

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
