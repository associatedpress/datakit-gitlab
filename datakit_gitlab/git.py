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
    def default_branch():
        """Name of the branch git creates on `init`.

        Honors the user's `init.defaultBranch` git config, falling back to
        `main` when it is unset (older gits default to `master`, but we prefer
        `main` when we have to guess).
        """
        try:
            branch = subprocess.check_output(
                ['git', 'config', 'init.defaultBranch']
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = ''
        return branch or 'main'

    @staticmethod
    def push():
        subprocess.check_output(['git', 'push', '-u', 'origin', Git.default_branch()])
