from gitlab import Gitlab


class GitlabProject:

    def __init__(self, gitlab_url, api_token, namespace, project_slug):
        self.gitlab_url = gitlab_url
        self.api_token = api_token
        self.namespace = namespace
        self.project_slug = project_slug
        self.client = Gitlab(self.gitlab_url, self.api_token, ssl_verify=False)

    @property
    def url(self):
        return "{}/{}/{}".format(
            self.gitlab_url,
            self.namespace,
            self.project_slug
        )

    def exists(self):
        return len(self.client.projects.list(search=self.project_slug)) > 0

    def create(self):
        grp = self.client.groups.list(search=self.namespace)[0]
        proj_metadata = {
            'name': self.project_slug,
            'namespace_id': grp.id
        }
        proj = self.client.projects.create(
            proj_metadata,
            retry_transient_errors = True
        )
        return proj

    def add_issue(self, opts):
        project = self.get_project()
        user = self.get_current_user()
        opts['assignee_id'] = user.id
        return project.issues.create(opts)

    def get_project(self):
        try:
            return self.project
        except AttributeError:
            arg = "{}/{}".format(self.namespace, self.project_slug)
            self.project = self.client.projects.get(arg)
            return self.project

    def get_current_user(self):
        self.client.auth()
        return self.client.user
