# -*- coding: utf-8 -*-
import os

from datakit import ConfigField

from datakit_gitlab.gitlab_project import GitlabProject


GITLAB_CONFIG_SPEC = [
    ConfigField('gitlab_url', required=True,
                help='Base URL of the GitLab instance (e.g. https://gitlab.com)'),
    ConfigField('default_namespace', required=True,
                help='GitLab namespace (user or group) new projects are created under'),
    ConfigField('api_key', required=True, secret=True, dedupe_prefix='glpat-',
                help='GitLab personal access token (api scope)'),
]


class ProjectMixin:

    "Mixin with code useful across plugin commands"

    plugin_slug = 'datakit-gitlab'

    config_spec = GITLAB_CONFIG_SPEC

    @property
    def project_slug(self):
        return os.path.basename(os.getcwd())

    def get_gitlab_project_client(self, project_slug):
        configs = self.configs
        url = configs['gitlab_url']
        namespace = configs['default_namespace']
        api_key = configs['api_key']
        return GitlabProject(url, api_key, namespace, project_slug)
