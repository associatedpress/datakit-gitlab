===============================
datakit-gitlab
===============================

Commands to manage project integration with Gitlab.

Features
========

* Runs initial git commands to bootstrap a project (init/add/commit)
* Creates Gitlab project
* Links local repo to newly created Gitlab project
* Pushes first commit to new Gitlab project

Usage
=====

This plugin should be used in tandem with `datakit-data`_.

After installing the plugin::

  # asuming you create a project called Foo
  $ datakit project:create 
  $ cd foo/
  $ datakit gitlab:integrate

Credits
========

This plugin was created with Cookiecutter_ and the `associatedpress/cookiecutter-datakit-plugin`_ 
project template (a modified version of the most excellent `audreyr/cookiecutter-pypackage`_).

.. _datakit-data: https://datakit-data.readthedocs.io/en/latest/
.. _datakit: https://github.com/associatedpress/datakit-core
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`associatedpress/cookiecutter-datakit-plugin`: https://github.com/associatedpress/cookiecutter-datakit-plugin
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
