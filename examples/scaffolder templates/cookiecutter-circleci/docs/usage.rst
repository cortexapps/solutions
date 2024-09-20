Advanced Usage
========================================================

For generate, or replace the `CircleCI`_ pipeline of a existing project, use the ``-f`` option, and use the foldername as ``project_slug``.

.. code:: bash

  cookiecutter https://github.com/nolte/cookiecutter-circleci.git --checkout develop


.. danger::

   Be carefull when the config are generated to a existing project. Existing files will be overwrite.


Creating the `.circleci/config.yml <https://circleci.com/docs/2.0/configuration-reference/#section=configuration>`_ Job Configuration.


Template Variables
---------------------------------------------------------

generate_tox_file
  generating a ``tox.ini`` build script

generate_sphinx_doc
  add required steps for generate sphinx documentation

project_slug
  project folder name

project_type
  | type of the project artefact, like cookiecutter, ansible roles, etc.
  | currently supported: ``cookiecutter``

.. include:: ./links.rst
