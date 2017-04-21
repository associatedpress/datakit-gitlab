# -*- coding: utf-8 -*-
import os

from datakit_gitlab.gitlab_project import GitlabProject


class ProjectMixin:

    "Mixin with code useful across plugin commands"

    plugin_slug = 'datakit-gitlab'

    @property
    def project_slug(self):
        return os.path.basename(os.getcwd())

    def get_gitlab_project_client(self, project_slug):
        configs = self.configs
        url = configs['gitlab_url']
        namespace = configs['default_namespace']
        api_key = configs['api_key']
        return GitlabProject(url, api_key, namespace, project_slug)
