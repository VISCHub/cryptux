# How to publish a library using PyPi

* Read http://peterdowns.com/posts/first-time-with-pypi.html
* Prepare & add credentials: `~/.pypirc`
* Sections for TEST is `testpypi` and for PROD is `pypi`
* Register credentials with `testpypi` & `pypi`
  * TEST: `python setup.py register -r testpypi`
  * PROD: `python setup.py register -r pypi`
* URL for TEST: https://test.pypi.org/legacy/
* Publish to PROD: `python setup.py sdist upload -r testpypi`
* URL for PROD: https://upload.pypi.org/legacy/
* Publish to PROD: `python setup.py sdist upload -r pypi`

## Sample Configuration

The content of `~/.pypirc`:

```
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
repository=https://upload.pypi.org/legacy/
username=prod.id
password=xxx

[testpypi]
repository=https://test.pypi.org/legacy/
username=test.id
password=xxx
```
