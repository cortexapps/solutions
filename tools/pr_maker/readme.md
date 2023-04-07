## PR Maker

This python script queries your cortex instance for all catalog entities. It then retrieves the yaml definition of the entity and finds the github repo. Once it has the repo, it uses the GitHub API via [PyGitHub](https://pypi.org/project/PyGithub/) to find the repo, create a branch, adding the cortex.yaml to it and opens a PR.

### Note

The script uses `main` as the default branch. If you are using another name, make sure to update the script.
Make sure the organization has it enabled to accept changes via GitHub API tokens, otherwise it may not work.