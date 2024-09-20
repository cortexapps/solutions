import pytest
import os


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    return chrome_options


def test_example(selenium):
    selenium.get(os.environ["SELENIUM_BASE_URL"])
    # selenium.save_screenshot('/tmp/screenshot/sample_screenshot_1.png');
    assert "Cookiecutter Template for circleci BuildJobs — Cookiecutter CircleCI Pipeline documentation" in selenium.title
