import os
from unittest import mock

import pytest

from ..conftest import read_fixture

from datakit_gitlab import Integrate
import responses
from responses import matchers


@responses.activate
def test_project_buildout(mocker, caplog, tmpdir):
    "Integrate should auto-generate Gitlab project"
    # Mock search query to check if project already exists. The v4 API passes
    # the project name as a `search` query param, so match on it to assert we
    # actually searched for `fake-project`.
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/projects',
        match=[matchers.query_param_matcher({'search': 'fake-project'}, strict_match=False)],
        body='[]',
        status=200,
        content_type='application/json'
    )
    # Mock group API call to resolve group ID based on name. Like the project
    # search, v4 passes the namespace as a `search` query param, so match on it
    # to assert we actually looked up the `data` group.
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/groups',
        match=[matchers.query_param_matcher({'search': 'data'}, strict_match=False)],
        body=read_fixture('group_id_lookup'),
        status=200,
        content_type='application/json'
    )
    # Mock project creation response
    responses.add(
        responses.POST,
        'https://gitlab.inside.ap.org/api/v4/projects',
        body=read_fixture('project_created-201'),
        status=201,
        content_type='application/json'
    )
    # Mock subprocess push and check that it was called
    mock_subprocess = mocker.patch(
        'datakit_gitlab.git.subprocess.check_output',
        autospec=True,
    )
    # Pin the detected default branch so the push target is deterministic
    mocker.patch(
        'datakit_gitlab.git.Git.default_branch',
        return_value='master',
    )
    cmd = Integrate(None, None)
    parsed_args = mock.Mock()
    cmd.run(parsed_args)
    assert 'Running Git initialization' in caplog.text
    expected_git_calls = [
        mocker.call(['git', 'init']),
        mocker.call(['git', 'add', '.']),
        mocker.call(['git', 'commit', '-m', 'Initial commit']),
        mocker.call(['git', 'remote', 'add', 'origin', 'git@gitlab.inside.ap.org:data/fake-project.git']),
        mocker.call(['git', 'push', '-u', 'origin', 'master'])
    ]
    assert mock_subprocess.call_args_list == expected_git_calls
    alert_msg = 'Project created: \n\thttps://gitlab.inside.ap.org/data/fake-project'
    assert alert_msg in caplog.text


@responses.activate
def test_project_already_exists(caplog):
    "Integrate should fail if project of same name already exists on Gitlab"
    # Mock search query to check if project already exists
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/projects',
        match=[matchers.query_param_matcher({'search': 'fake-project'}, strict_match=False)],
        body=read_fixture('project_search-already_exists'),
        status=200,
        content_type='application/json'
    )
    cmd = Integrate(None, None)
    parsed_args = mock.Mock()
    cmd.run(parsed_args)
    assert 'ERROR: fake-project already exists on Gitlab!' in caplog.text


def test_missing_config(set_gitlab_config, caplog):
    "Integrate should bail before touching Gitlab when no config is present"
    set_gitlab_config({})
    Integrate(None, None).run(mock.Mock())
    assert 'ERROR: datakit-gitlab config not found!' in caplog.text


def test_empty_project(caplog):
    "Integrate should refuse to commit a directory with nothing in it"
    os.remove('README.md')
    Integrate(None, None).run(mock.Mock())
    assert 'ERROR: Project is empty, nothing to commit' in caplog.text


def test_missing_required_config_keys(set_gitlab_config, caplog):
    "A truthy-but-incomplete config should abort with guidance, not a stack trace"
    set_gitlab_config({'gitlab_url': 'https://gitlab.inside.ap.org'})
    with pytest.raises(SystemExit):
        Integrate(None, None).run(mock.Mock())
    assert 'missing required keys: default_namespace, api_key' in caplog.text
    assert 'datakit config init datakit-gitlab' in caplog.text


@responses.activate
def test_existing_git_repo(mocker, caplog):
    "With a repo already initialized, Integrate skips git init and just publishes"
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/projects',
        match=[matchers.query_param_matcher({'search': 'fake-project'}, strict_match=False)],
        body='[]',
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/groups',
        match=[matchers.query_param_matcher({'search': 'data'}, strict_match=False)],
        body=read_fixture('group_id_lookup'),
        status=200,
        content_type='application/json'
    )
    responses.add(
        responses.POST,
        'https://gitlab.inside.ap.org/api/v4/projects',
        body=read_fixture('project_created-201'),
        status=201,
        content_type='application/json'
    )
    os.mkdir('.git')
    mock_subprocess = mocker.patch(
        'datakit_gitlab.git.subprocess.check_output',
        autospec=True,
    )
    mocker.patch('datakit_gitlab.git.Git.default_branch', return_value='main')
    Integrate(None, None).run(mock.Mock())
    assert 'Git repo found, creating Gitlab project' in caplog.text
    assert mock_subprocess.call_args_list == [
        mocker.call(['git', 'remote', 'add', 'origin', 'git@gitlab.inside.ap.org:data/fake-project.git']),
        mocker.call(['git', 'push', '-u', 'origin', 'main'])
    ]
