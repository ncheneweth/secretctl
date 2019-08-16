# secretctl
Command-line tool and module for working with aws secrets manager

$ secretctl

commands:

$ export --output [json(default), yaml, dotenv, tfvars]

no support for (custom pki key)
no support for binary secret value type
no mock support for testing descriptions or resource tags

---
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

cc-test-reporter before-build
cc-test-reporter after-build
