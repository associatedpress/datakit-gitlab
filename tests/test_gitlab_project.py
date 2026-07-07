from datakit_gitlab.gitlab_project import GitlabProject


def test_url_joins_instance_namespace_and_slug():
    project = GitlabProject(
        'https://gitlab.inside.ap.org', 'token', 'data', 'fake-project'
    )
    assert project.url == 'https://gitlab.inside.ap.org/data/fake-project'
