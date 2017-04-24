# -*- coding: utf-8 -*-
from cliff.command import Command
from datakit import CommandHelpers

from datakit_gitlab.project_mixin import ProjectMixin


class Add(ProjectMixin, CommandHelpers, Command):
    "Quickly add tickets to Gitlab project"

    def get_parser(self, prog_name):
        parser = super(Add, self).get_parser(prog_name)
        parser.add_argument(
            '-t',
            '--title',
            help="Short title for Issue that must be wrapped in quotes"
        )
        return parser

    def take_action(self, parsed_args):
        client = self.get_gitlab_project_client(self.project_slug)
        resp = client.add_issue({
            'title': parsed_args.title.strip()
        })
        self.log.info("Created issue #{}: {}".format(resp.iid, resp.web_url))
