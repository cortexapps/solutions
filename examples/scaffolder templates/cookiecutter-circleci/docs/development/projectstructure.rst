Project Structure
========================================================

Base Directory Structure
------------------------------------------------------

`.bumpversion.cfg`
  Config file for `bumpversion`_ handled the `semantic versioning`_ process. More information at the :ref:`development-process` description.

`.circleci/config.yml`
  | Used `CircleCI`_ for handle the :ref:`development-process-build`, :ref:`development-process-test`, :ref:`development-process-release` and :ref:`development-process-publish` steps.
  | **Status:** |CircleCI build status|

`ci-scripts`
  Folder for ci utility scripts like, install selenium.

`docs`
  | This project is documentated with `sphinx-doc`_. The generated deployment will be published to `ReadTheDocs` and `nolte.github.io`.
  | **Status:** |Documentation Status|

`.github`
  This folder is used form the `GitHub Issue Templates <https://blog.github.com/2016-02-17-issue-and-pull-request-templates/>`_.

`it-tests`
  This Folder contains `Selenium`_ based `pytest`_ integrations tests. Runned after a `nolte.github.io/cookiecutter-circleci <https://nolte.github.io/cookiecutter-circleci/>`_ deployment.

`tests`
  Test for checking the CookieCutter Template generated projects, based on `pytest`_ and `pytest-cookies <https://github.com/hackebrot/pytest-cookies>`_.

`tox.ini`
  Using `tox`_ for handle the different build and test configs.

  .. list-table:: Important Tox Environments
     :header-rows: 1

     * - Tox Environment
       - Description
     * - {py27,py36}-test
       - Start the local builds, used `pytest-cookies`_ for testing the `cookiecutter`_ template, see :ref:`development-process-test-unit`.
     * - docs
       - Generate the html `sphinx-doc`_. All required dependencies are listed in `requirementsDocs.txt`
     * - py36-{github,readthedocs-latest,readthedocs-stable}-integrationtests
       - Start the Selenium Integration Tests for existing deployments, some type of Smoke Tests, see :ref:`development-process-test-integrationtest`.


`.travis.yml`
  | Build config for the `TravisCI`_ Job, used for testing different python versions.
  | **Status:** |Travis CI build status|

.. _sphinx-doc: `link-sphinx`_

.. include:: ../links.rst
