# -*- coding: utf-8 -*-
import os

from cliff.command import Command
from datakit import CommandHelpers
from datakit_gitlab.git import Git
from datakit_gitlab.gitlab_project import GitlabProject


class Integrate(CommandHelpers, Command):
    "Integrate local project code with Gitlab"

    plugin_slug = 'datakit-gitlab'

    def take_action(self, parsed_args):
        if not bool(self.configs):
            msg = "ERROR: datakit-gitlab config not found!"
            self.log.error(msg)
            return
        if os.listdir() == ['.git'] or not bool(os.listdir()):
            msg = "ERROR: Project is empty, nothing to commit"
            self.log.error(msg)
            return
        proj_slug = self.get_project_slug()
        project = self.get_gitlab_project_client(proj_slug)
        if project.exists():
            msg = "ERROR: {} already exists on Gitlab!".format(proj_slug)
            self.log.error(msg)
            return
        # Guard against re-initialization
        if Git.is_repository() is False:
            self.log.info("Running Git initialization...")
            Git.init()
            Git.add()
            Git.commit()
        else:
            self.log.info("Git repo found, creating Gitlab project")
        resp = project.create()
        self.log.info(dir(resp))
        Git.remote_add_origin(resp.ssh_url_to_repo)
        Git.push()
        alert_msg = "Project created: \n\t{}".format(resp.web_url)
        self.log.info(alert_msg)

    def get_project_slug(self):
        return os.path.basename(os.getcwd())

    def get_gitlab_project_client(self, project_slug):
        configs = self.configs
        if 'gitlab_url' not in configs.keys():
            err_msg = "ERROR: datakit-gitlab config missing Gitlab URL!"
            self.log.error(err_msg)
            raise SystemExit
        if 'default_namespace' not in configs.keys():
            err_msg = "ERROR: datakit-gitlab config missing default namespace!"
            self.log.error(err_msg)
            raise SystemExit
        if 'api_key' not in configs.keys():
            err_msg = "ERROR: datakit-gitlab config missing API key!"
            self.log.error(err_msg)
            raise SystemExit
        url = configs['gitlab_url']
        namespace = configs['default_namespace']
        api_key = configs['api_key']
        return GitlabProject(url, api_key, namespace, project_slug)
