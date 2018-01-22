from unittest import mock

from ..conftest import read_fixture

from datakit_gitlab import Integrate
import responses


@responses.activate
def test_project_buildout(mocker, caplog, tmpdir):
    "Integrate should auto-generate Gitlab project"
    # Mock search query to check if project already exists
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v3/projects/search/fake-project',
        body='[]',
        status=200,
        content_type='application/json'
    )
    # Mock group API call`to group ID based on name
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v3/groups/data',
        body=read_fixture('group_id_lookup'),
        status=200,
        content_type='application/json'
    )
    # Mock project creation response
    responses.add(
        responses.POST,
        'https://gitlab.inside.ap.org/api/v3/projects',
        body=read_fixture('project_created-201'),
        status=201,
        content_type='application/json'
    )
    # Mock subprocess push and check that it was called
    mock_subprocess = mocker.patch(
        'datakit_gitlab.git.subprocess.check_output',
        autospec=True,
    )
    cmd = Integrate(None, None, cmd_name='gitlab integrate')
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
        'https://gitlab.inside.ap.org/api/v3/projects/search/fake-project',
        body=read_fixture('project_search-already_exists'),
        status=200,
        content_type='application/json'
    )
    cmd = Integrate(None, None, cmd_name='gitlab integrate')
    parsed_args = mock.Mock()
    cmd.run(parsed_args)
    assert 'ERROR: fake-project already exists on Gitlab!' in caplog.text
