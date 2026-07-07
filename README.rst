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


Install this plugin alongside datakit-core_. The recommended way is with uv_,
which keeps the ``datakit`` command and its plugins in a single isolated
environment::

  $ uv tool install datakit-core --with datakit-gitlab

See the datakit-core_ docs for other ways to install and combine plugins.

Next, configure the plugin with the generic ``datakit config`` command family
that ships with datakit-core_. The quickest way is to fill in every value
interactively (the access token is entered hidden)::

  $ datakit config init datakit-gitlab

This prompts for three values:

``gitlab_url``
  The base URL of your GitLab instance (e.g. ``https://gitlab.com``).

``default_namespace``
  Your user name or the organization namespace new projects are created under.

``api_key``
  Your GitLab Personal Access Token.

You can also set an individual value, and check that the token authenticates::

  $ datakit config set datakit-gitlab gitlab_url https://gitlab.com
  $ datakit config verify datakit-gitlab

``datakit config`` writes ``~/.datakit/plugins/datakit-gitlab/config.json`` for
you, so there's no need to hand-edit that file.

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
.. _datakit-core: https://datakit-core.readthedocs.io/en/latest/
.. _uv: https://docs.astral.sh/uv/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`associatedpress/cookiecutter-datakit-plugin`: https://github.com/associatedpress/cookiecutter-datakit-plugin
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
