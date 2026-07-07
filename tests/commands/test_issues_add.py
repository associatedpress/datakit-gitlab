import json
import re
from unittest import mock

import pytest

from ..conftest import read_fixture

from datakit_gitlab.commands.issues import Add
import responses


def test_parser_requires_title():
    "--title is mandatory; omitting it is an argparse error"
    parser = Add(None, None).get_parser('gitlab issues add')
    assert parser.parse_args(['--title', 'A ticket']).title == 'A ticket'
    with pytest.raises(SystemExit):
        parser.parse_args([])


@responses.activate
def test_add_issue(caplog):
    "Add creates an issue on the resolved project, assigned to the current user"
    # The project is assumed to already exist on Gitlab.
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/projects/data%2Ffake-project',
        body=read_fixture('project_get'),
        status=200,
        content_type='application/json'
    )
    # `current_user_get` reports the authenticated user as id 284.
    responses.add(
        responses.GET,
        'https://gitlab.inside.ap.org/api/v4/user',
        body=read_fixture('current_user_get'),
        status=200,
        content_type='application/json'
    )
    issue_creation = re.compile(r'https://gitlab\.inside\.ap\.org/api/v4/projects/\d+/issues')
    responses.add(
        responses.POST,
        issue_creation,
        body=read_fixture('issue_added_201'),
        status=201,
        content_type='application/json'
    )
    parsed_args = mock.Mock()
    parsed_args.title = "  Do some data stuff  "
    Add(None, None).run(parsed_args)

    posted = next(c for c in responses.calls if c.request.method == 'POST')
    body = json.loads(posted.request.body)
    assert body['title'] == 'Do some data stuff'
    assert body['assignee_id'] == 284
    assert 'Created issue #3: https://gitlab.inside.ap.org/data/fake-project/issues/3' in caplog.text
