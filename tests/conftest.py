import os
import pytest
from datakit.utils import mkdir_p, write_json


@pytest.fixture
def dkit_home(tmpdir):
    return os.path.join(tmpdir.strpath, '.datakit')


@pytest.fixture
def fake_project(tmpdir):
    return os.path.join(tmpdir.strpath, 'fake-project')


@pytest.fixture(autouse=True)
def bootstrap_temp_env(dkit_home, fake_project, monkeypatch, tmpdir):
    mkdir_p(dkit_home)
    mkdir_p(fake_project)
    monkeypatch.setenv('DATAKIT_HOME', dkit_home)
    monkeypatch.chdir(fake_project)
    create_readme(fake_project)
    create_plugin_config(
        dkit_home,
        'datakit-gitlab',
        {
            "gitlab_url": 'https://gitlab.inside.ap.org',
            "api_key": "afdafsa",
            "default_namespace": "data"
        }
    )


def create_readme(fake_project_pth):
    readme = os.path.join(fake_project_pth, "README.md")
    content = "Example readme for a stub project"
    with open(readme, 'w') as fh:
        fh.write(content)


def create_plugin_config(dkit_home, project_name, content):
    plugin_dir = os.path.join(dkit_home, 'plugins', project_name)
    mkdir_p(plugin_dir)
    config_file = os.path.join(plugin_dir, 'config.json')
    write_json(config_file, content)
    return content


def create_project_config(project_root, contents={}):
    config_dir = os.path.join(project_root, 'config')
    mkdir_p(config_dir)
    project_config = os.path.join(config_dir, 'datakit-data.json')
    write_json(project_config, contents)


def dir_contents(path):
    dirs_and_files = []
    for root, subdirs, files in os.walk(path):
        for directory in subdirs:
            dirs_and_files.append(directory)
            for fname in files:
                dirs_and_files.append(os.path.join(directory, fname))
    return dirs_and_files


def read_fixture(name):
    tests_dir = os.path.dirname(__file__)
    fixture_pth = os.path.join(tests_dir, "fixtures/{}.json".format(name))
    with open(fixture_pth, 'r') as fh:
        return fh.read()
