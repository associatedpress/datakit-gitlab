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
        return len(self.client.projects.search(self.project_slug)) > 0

    def create(self):
        grp = self.client.groups.get(self.namespace)
        proj = self.client.projects.create({
            'name': self.project_slug,
            'namespace_id': grp.id
        })
        return proj
