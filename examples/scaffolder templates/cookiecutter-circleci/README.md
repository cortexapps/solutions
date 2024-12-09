This cookiecutter template is based on [this](https://github.com/nolte/cookiecutter-circleci) template.

This template adds a new CircleCI configuration file to an existing repository. Since this template adds a file to an existing repository, it creates a PR against the repo.

Cortex does not support cookiecutter hooks, so all hooks have been removed.


# Cookiecutter Template for circleci BuildJobs

[Cookiecutter Template](https://cookiecutter.readthedocs.io) for a [CircleCI](https://circleci.com/), [Continuous integration](https://en.wikipedia.org/wiki/Continuous_integration)/[Continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery) Pipeline, for different types of projects. Using [Tox](https://tox.readthedocs.io/en/latest/config.html) for abstraction the the Process workflow, from the project specific buildsteps.

**Current Version:** 0.13.0-dev

**Result**
```
.
└── cookiecutter-example-build
    ├── .circleci
    │   └── config.yml
    ├── docsRequirements.txt
    └── tox.ini

2 directories, 3 files
```
