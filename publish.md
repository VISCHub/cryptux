# How to publish a library using PyPi

* Read http://peterdowns.com/posts/first-time-with-pypi.html
* Prepare & add credentials: `~/.pypirc`
* The section for TEST is `testpypi` and for PROD is `pypi`
* Publish to TEST:
  * Register: `python setup.py register -r testpypi`
  * API end-point: https://test.pypi.org/legacy/
  * Command: `python setup.py sdist upload -r testpypi`
* Publish to PROD:
  * Register: `python setup.py register -r pypi`
  * API end-point: https://upload.pypi.org/legacy/
  * Command: `python setup.py sdist upload -r pypi`

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
