To release a new version of qtconsole you need to follow these steps:

* Update docs/source/changelog.rst with a PR.

* Close the current milestone on Github

* git pull or git fetch/merge

* git clean -xfdi

* Update version in `_version.py` (set release version, remove 'dev0')

* git add and git commit with `Release X.X.X`

* python setup.py sdist upload

* activate pyenv-with-latest-setuptools && python setup.py bdist_wheel upload

* git tag -a X.X.X -m 'Release X.X.X'

* Update version in `_version.py` (add 'dev0' and increment minor)

* git push upstream master

* git push upstream --tags
