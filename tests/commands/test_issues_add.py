import re
from unittest import mock

from ..conftest import read_fixture

from datakit_gitlab.commands.issues import Add
import responses


@responses.activate
def test_add_issue(mocker, caplog, tmpdir):
    # Mock GET for project meta (assumged to already exist)
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v3/projects/data%2Ffake-project',
        body=read_fixture('project_get'),
        status=200,
        content_type='application/json'
    )
    # Mock API call to get current user info
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v3/user',
        body=read_fixture('current_user_get'),
        status=200,
        content_type='application/json'
    )
    # Mock project creation response
    post_re = re.compile(r'https://gitlab\.inside\.ap\.org/api/v3/projects/\d+/issues/')
    responses.add(
        responses.POST,
        post_re,
        body=read_fixture('issue_added_201'),
        status=201,
        content_type='application/json'
    )
    cmd = Add(None, None, cmd_name='gitlab issues add')
    parsed_args = mock.Mock()
    parsed_args.title = "Do some data stuff"
    cmd.run(parsed_args)
    assert re.search(r'Created issue #\d: https://gitlab.inside.ap.org/data/fake-project/issues/\d', caplog.text)
    assert 'assignee_id' in responses.calls[2].request.body
