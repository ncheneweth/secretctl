# secretctl
Command-line tool and module for working with aws secrets manager

$ secretctl

commands:

$ export --output [json(default), yaml, dotenv, tfvars] ( dotenv is KEY=value, tfvars is KEY = "value" )

no support for kms_key_id (custom pki key)
no support for binary secret value type
no mock support for testing descriptions or resource tags

---
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
