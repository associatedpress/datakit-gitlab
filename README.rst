===============================
DataKit Gitlab plugin
===============================

Commands to manage project integration with Gitlab.

Features
========

* Runs initial git commands to bootstrap a project (init/add/commit)
* Creates Gitlab project
* Links local repo to newly created Gitlab project
* Pushes first commit to new Gitlab project

Setup instructions
==================


Assuming you have datakit_ installed, run the following to install the
`datakit-gitlab` plugin::

  $ pip install datakit-gitlab

Create a configuration file at ``~/.datakit/plugins/datakit-gitlab/config.json`` with the following structure::

    {
      "gitlab_url": "GITLAB_URL",
      "default_namespace": "YOUR_NAMESPACE",
      "api_key": "PERSONAL_ACCESS_TOKEN"
    }

``GITLAB_URL`` is the URL of your Gitlab instance.

``YOUR_NAMESPACE`` is your user name or the organization namespace.

``PERSONAL_ACCESS_TOKEN`` is your Personal Access Token.

Gitlab Personal Access Tokens can be obtained under User Settings > Access Tokens. You will need to make a token with both api and sudo privileges. More information on Gitlab Personal Access Tokens can be found here: https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html

Usage
=====

This plugin should be used in tandem with `datakit-project`_.

Project creation
-----------------

After installing the plugin::

  # Assuming you create a local project called Foo
  $ datakit project create
  $ cd foo/
  $ datakit gitlab integrate

Creating issues
---------------

You can quickly create a new issue using the following command::

  $ cd foo/
  $ datakit gitlab issues add --title "Some new issue"


Credits
========

This plugin was created with Cookiecutter_ and the `associatedpress/cookiecutter-datakit-plugin`_ 
project template (a modified version of the most excellent `audreyr/cookiecutter-pypackage`_).

.. _datakit-project: https://datakit-project.readthedocs.io/en/latest/
.. _datakit: https://github.com/associatedpress/datakit-core
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`associatedpress/cookiecutter-datakit-plugin`: https://github.com/associatedpress/cookiecutter-datakit-plugin
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
