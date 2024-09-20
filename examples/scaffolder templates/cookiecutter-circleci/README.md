# Cookiecutter Template for circleci BuildJobs

[![TravisCIBuildStatus](https://travis-ci.org/nolte/cookiecutter-circleci.svg?branch=develop)](https://travis-ci.org/nolte/cookiecutter-circleci) [![CircleCIBuildStatus](https://circleci.com/gh/nolte/cookiecutter-circleci.svg?style=svg)](https://circleci.com/gh/nolte/cookiecutter-circleci) [![DocumentationStatus](https://readthedocs.org/projects/cookiecutter-circleci/badge/?version=latest)](https://cookiecutter-circleci.readthedocs.io/en/latest/?badge=latest) [![GitHubProjectStars](https://img.shields.io/github/stars/nolte/cookiecutter-circleci.svg?label=Stars&style=social)](https://github.com/nolte/cookiecutter-circleci) [![GitHubIssueTracking](https://img.shields.io/github/issues-raw/nolte/cookiecutter-circleci.svg)](https://github.com/nolte/cookiecutter-circleci) [![GitHubLatestRelease](https://img.shields.io/github/release/nolte/cookiecutter-circleci.svg)](https://github.com/nolte/cookiecutter-circleci) [![CodeFactor](https://www.codefactor.io/repository/github/nolte/cookiecutter-circleci/badge)](https://www.codefactor.io/repository/github/nolte/cookiecutter-circleci)


[Cookiecutter Template](https://cookiecutter.readthedocs.io) for a [CircleCI](https://circleci.com/), [Continuous integration](https://en.wikipedia.org/wiki/Continuous_integration)/[Continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery) Pipeline, for different types of projects. Using [Tox](https://tox.readthedocs.io/en/latest/config.html) for abstraction the the Process workflow, from the project specific buildsteps.

**Current Version:** 0.13.0-dev

## Features

* Handle [Semantic Versioning](https://semver.org/) of the project. (*planed*)
* Create a [Github Releases](https://help.github.com/articles/creating-releases/). (*planed*)
* Push generated [sphinx](http://www.sphinx-doc.org/en/master/) page to [GithubPage](https://pages.github.com/). (*planed*)
* Create GitHub Based Cangelog with [ferrarimarco/docker-github-changelog-generator](https://github.com/ferrarimarco/docker-github-changelog-generator). (*planed*)


## Usage

Install [cookiecutter](https://pypi.org/project/cookiecutter/) to your local machine.

**Example usage**
```
(cookiecutter) $ cookiecutter https://github.com/nolte/cookiecutter-circleci.git
generate_tox_file [n]: y
generate_sphinx_doc [n]: y
project_slug []: cookiecutter-example-build
Select project_type:
1 - cookiecutter
Choose from 1 [1]: 1
```

**Result**
```
(cookiecutter) $ tree
.
└── cookiecutter-example-build
    ├── .circleci
    │   └── config.yml
    ├── docsRequirements.txt
    └── tox.ini

2 directories, 3 files
```
