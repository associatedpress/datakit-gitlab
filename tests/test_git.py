import subprocess

from datakit_gitlab.git import Git


def test_default_branch_honors_git_config(mocker):
    "The configured init.defaultBranch wins when git reports one"
    mocker.patch(
        'datakit_gitlab.git.subprocess.check_output',
        return_value=b'trunk\n',
    )
    assert Git.default_branch() == 'trunk'


def test_default_branch_falls_back_when_config_empty(mocker):
    "An unset (empty) init.defaultBranch falls back to main"
    mocker.patch(
        'datakit_gitlab.git.subprocess.check_output',
        return_value=b'\n',
    )
    assert Git.default_branch() == 'main'


def test_default_branch_falls_back_when_config_unset(mocker):
    "A non-zero git exit (config key absent) falls back to main"
    mocker.patch(
        'datakit_gitlab.git.subprocess.check_output',
        side_effect=subprocess.CalledProcessError(1, 'git'),
    )
    assert Git.default_branch() == 'main'
