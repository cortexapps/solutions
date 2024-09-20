 .. _development-process:

Development Process
========================================================

.. _development-process-branch-model:

Branch Modell
------------------------------------------

As Branchmodel we use a mix of `Gitflow <https://datasift.github.io/gitflow/IntroducingGitFlow.html>`_ and `pull-requests <https://help.github.com/articles/about-pull-requests/>`_.
Gitflow is used for the Release Process, the ``master`` branch present the latest Published Release.
PullRequests are used for integrate external changes and ``feature`` branches into the :ref:`development-process-branch-model-develop`.


Feature Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New features will be develop in feature branches like ``feature/integrate-cuberite``.

.. warning::

	Please dont use use ``feature/*`` branches in your production Environment.


.. _development-process-branch-model-develop:

Develop Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``develop`` branch contains the latest unrelesed version from the template, mostly stable ;)

.. _development-process-branch-model-release:

Release Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Master Branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``master`` present the latest published release.


.. _development-process-build:

Build
--------------------------------------------------------



.. _development-process-test:

Testing
----------------------------------------------------

Static tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the Static Tests we use `flake8 <http://flake8.pycqa.org/en/latest/>`_, this will check the style.
The cofiguration can found at the `tox.ini`

.. _development-process-test-unit:

Unit tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _development-process-test-integrationtest:

Integrations tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



.. _development-process-release:

Releasing
----------------------------------------------------

You can start the Release process with some commit like:

.. code:: bash

  git commit --allow-empty -m "[GradeUP][skip travis] grade up the branch"
  git push origin develop

| With pushing this commit the Release Pipeline will started automatically.
| **The Process**

* Update the version to new Release, see :ref:`development-process-release-versioning`
* create the :ref:`development-process-branch-model-release`
* prepare the :ref:`development-process-branch-model-develop` branch for next version.
* Create :ref:`development-process-publish-gh-release`
* Publish :ref:`development-process-publish-gh-page`
* execute :ref:`development-process-test-integrationtest`
* delete the :ref:`development-process-branch-model-release`


.. _development-process-release-versioning:

Versioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This project follows `semantic versioning`_.
| In the context of semantic versioning, consider the role contract to be defined by the role variables.

-  Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
-  Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
-  Bug fixes will increase the **patch** version.

.. _development-process-publish:

Publishing
----------------------------------------------------

.. _development-process-publish-gh-release:

Github Release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _development-process-publish-gh-page:

Github Page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../links.rst
