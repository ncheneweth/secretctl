"""cli commands"""
import json
import sys
from invoke import task
from secretctl.validators import validate_path, tags_to_json, set_secret, read_value
from secretctl.tuples import Secret, create_secret, update_secret, get_secret, tag_secret, untag_secret, list_secrets
from secretctl.output import print_read, print_list, print_export



@task(optional=['isjson', 'description', 'tags'])
def create(_ctx, path, value, isjson=False, description=None, tags=None):
    """add new path/key:value to Secrets Manager

       $> secretctl create <path> <value | - [--isjson]>
       <path> created

       Flags:

         --description STRING        Add a description to new secret.

         --tags <tag>=<value>, ...   Include tags with new secret.

         - [--isjson]                Read value from stdin. Include --isjson to validate json string.

                                     $> cat <filename> | secretctl create myapp/dev/public-key -
                                     myapp/dev/public-key created
    """
    secret_kwargs = {}
    secret_kwargs['path'] = validate_path(path)
    secret_kwargs['value'] = read_value(path, value, isjson)
    secret_kwargs['description'] = description
    if tags:
        secret_kwargs['tags'] = tags_to_json(tags)
    resp = create_secret(**secret_kwargs)
    print(f"{resp.path} created")

@task(optional=['isjson', 'description'])
def update(_ctx, path, value, isjson=False, description=None):
    """update secret value [Flags]

       $> secretctl update <path> <value | - [--isjson]> [Flags]
       <path> updated

       Flags:

         --description STRING        Update description of secret.

         - [--isjson]                Read value from stdin. Include --isjson to validate json string.

                                     $> cat <filename> | secretctl update myapp/dev/public-key -
                                     myapp/dev/public-key updated
    """
    secret_kwargs = {}
    secret_kwargs['path'] = validate_path(path)
    secret_kwargs['value'] = read_value(path, value, isjson)
    secret_kwargs['description'] = description
    resp = update_secret(**secret_kwargs)
    print(f"{resp.path} updated")

@task(optional=['quiet', 'info'])
def read(_ctx, path, quiet=False, info=False):
    """read secret from Secrets Manager [Flags]

       $>  secretctl read myapp/dev/docker_login
       Path/Key                   Version   Value
       myapp/dev/docker_login     1         mydockerlogin

       Flags:

         --quiet            Return only the secret value. Useful for working with secrets in pipelines.
                            Ex: Set DOCKER_LOGIN = to secret

                            $>  export DOCKER_LOGIN=$(secretctl read myapp/dev/docker_login -q)
                            $>  echo $DOCKER_LOGIN
                            mydockerlogin

         --info             Show description and tags.

    """
    print_read(get_secret(validate_path(path)), quiet=quiet, info=info)


@task
def tag(_ctx, path, tags):
    """add tag(s) to secret

    $>  secretctl tag myapp/dev/docker_login 'new_tag=value'
    myapp/dev/docker_login tagged
    """
    secret_kwargs = {}
    secret_kwargs['path'] = validate_path(path)
    secret_kwargs['tags'] = tags_to_json(tags)
    resp = tag_secret(**secret_kwargs)
    print(f"{resp.path} tagged")

@task
def untag(_ctx, path, tags):
    """remove tag(s) from secret

    $>  secretctl untag myapp/dev/docker_login 'new_tag'
    tags removed from myapp/dev/docker_login
    """
    secret_kwargs = {}
    secret_kwargs['path'] = validate_path(path)
    secret_kwargs['tags'] = tags_to_json(tags, novalue=True)
    resp = untag_secret(**secret_kwargs)
    print(f"tags removed from {resp.path}")

#pylint: disable=W0622
@task(optional=['path', 'tags'])
def list(_ctx, path=None, tags=None):
    """list secrets from Secrets Manager

    $> secretctl list myapp/dev

       Flags:

         --path STRING      Returns the subset of secrets with path STRING.
                            Ex: lists all the secrets for the dev environment of myapp

                            $>  secretctl list -p myapp/dev
                            Path/Key                   Version   Updated               Description
                            myapp/dev/docker_login     1         2019-07-28 19:09:55   private docker registry login
                            myapp/dev/docker_password  3         2019-07-29 11:54:18   private docker registry

         --tags STRING      Filter secrets by Tag STRING. Will includes tags with Keys or Values that 'contain' STRG.
                            Ex: lists all the secrets with a Tag containing a team's name, "bravo"

                            $>  secretctl list -t bravo
                            Path/Key              Version   Updated               Tags
                            app/dev/some_secret   1         2019-03-07 09:39:15   [{'Key': 'team', 'Value': 'bravo'}]
                            app/qa/secret         3         2019-04-22 12:04:21
    """
    path = validate_path(path) if path else path
    secrets = []
    for secret in list_secrets():
        if not path or (path and secret['Name'].startswith(path)):
            if not tags or ('Tags' in secret and tags in json.dumps(secret['Tags'])):
                secrets.append(set_secret(secret))

    if len(secrets) >= 1:
        print_list(secrets)
        print(f"Found {len(secrets)} secrets.")
    else:
        print('secretctl: no secrets match filter')

@task(optional=['output'])
def export(_ctx, path, output='tfvars'):
    """export formatted list of secrets [Flags]

       Flags:

         --output [option]  Returns the subset of secrets with path STRING.
                            Ex: lists all the secrets for the dev environment of myapp

                            $>  secretctl list -p myapp/dev
                            Path/Key                   Version   Updated               Description
                            myapp/dev/docker_login     1         2019-07-28 19:09:55   private docker registry login
                            myapp/dev/docker_password  3         2019-07-29 11:54:18   private docker registry

    """
    path = validate_path(path) if path else path
    secrets = []

    for id in list_secrets():
        secret = None
        # assess secrets matching path value, or all if none
        if not path:
            secret = id['Name']
        elif path and id['Name'].startswith(path):
            secret = id['Name']

        # if --tag <value> then return only keys on path where <value> is in tag
        if secret:
            secrets.append(get_secret(secret))

    if len(secrets) >= 1:
        print_export(secrets, output=output)
    else:
        print('secretctl: no secrets match filter')
