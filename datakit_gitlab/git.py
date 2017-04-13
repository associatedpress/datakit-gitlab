import os
import subprocess


class Git:

    @staticmethod
    def is_repository():
        return os.path.exists('.git')

    @staticmethod
    def init():
        subprocess.check_output(['git', 'init'])

    @staticmethod
    def add():
        subprocess.check_output(['git', 'add', '.'])

    @staticmethod
    def commit():
        subprocess.check_output(['git', 'commit', '-m', 'Initial commit'])

    @staticmethod
    def remote_add_origin(repo_url):
        subprocess.check_output(['git', 'remote', 'add', 'origin', repo_url])

    @staticmethod
    def push():
        subprocess.check_output(['git', 'push', '-u', 'origin', 'master'])
