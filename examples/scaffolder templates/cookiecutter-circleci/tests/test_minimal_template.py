import filecmp


def test_bake_project(cookies):
    result = cookies.bake(extra_context={'project_slug': 'simple'})
    verfiy_base_project_attributes(result, 'simple')


def test_bake_project_with_tox_ini(cookies):
    testconfig = {'project_slug': 'simplewithtox', 'generate_tox_file': 'y'}
    result = cookies.bake(extra_context=testconfig)
    verfiy_base_project_attributes(result, 'simplewithtox')
    tox_file = result.project.join('tox.ini')
    assert filecmp.cmp(str(tox_file), 'tests/golden_files/minimal/tox.ini', shallow=0)
    assert result.project.join('docsRequirements.txt').check(exists=0)

    circleci_job_file = result.project.join('.circleci/config.yml')
    assert circleci_job_file.isfile()
    assert filecmp.cmp(str(circleci_job_file), 'tests/golden_files/minimal/config.yml', shallow=0)


def test_bake_project_with_tox_ini_and_sphinx(cookies):
    testconfig = {'project_slug': 'simplewithtox', 'generate_tox_file': 'y', 'generate_sphinx_doc': 'y'}
    result = cookies.bake(extra_context=testconfig)
    verfiy_base_project_attributes(result, 'simplewithtox')
    tox_file = result.project.join('tox.ini')

    assert tox_file.isfile()
    assert filecmp.cmp(str(tox_file), 'tests/golden_files/sphinx/tox.ini', shallow=0)
    circleci_job_file = result.project.join('.circleci/config.yml')
    assert circleci_job_file.isfile()
    assert filecmp.cmp(str(circleci_job_file), 'tests/golden_files/sphinx/config.yml', shallow=0)
    assert result.project.join('docsRequirements.txt').check(exists=1)


def verfiy_base_project_attributes(result, expectedProjectName):
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == expectedProjectName
    assert result.project.isdir()
