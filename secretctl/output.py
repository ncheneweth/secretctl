"""cli output formatters"""
import json
from colorama import init, Fore
from secretctl.validators import json_to_tags
init(autoreset=True)

# print formatted results of read to stdout
def print_read(secret, quiet=False, info=False):
    """format secretctl read response"""
    options = {True: print_read_quiet, False: print_read_normal}
    options[quiet](secret, info)

def print_read_quiet(secret, _=False):
    """read quiet"""
    for _, value in secret.value.items():
        print(value)

def print_read_normal(secret, info=False):
    """format normal output from read"""
    col_path = len(secret.path) + 3
    print(Fore.YELLOW + "{:{wid}} {:<9} {}".format('Path/Key', 'Version', 'Value', wid=col_path))
    # output full json when the secret is multiple key:value pairs
    _value = json.dumps(secret.value) if len(secret.value) >= 2 else next(iter(secret.value.values()))
    print("{:{wid}} {:<9} {}".format(secret.path, secret.versions, _value, wid=col_path))
    if info:
        _desc = secret.description if secret.description else 'No description'
        _tags = json_to_tags(secret.tags) if secret.tags else 'No tags'
        print("{:{wid}} {}".format('*Desc', _desc, wid=col_path+10))
        print("{:{wid}} {}".format('*Tags', _tags, wid=col_path+10))

# print formatted results of list to stdout
def print_list(secrets):
    """format secretctl list response"""
    path_col = max(len(secret.path) for secret in secrets) + 3
    desc_col = desc_col_length(secrets)

    print(Fore.YELLOW + "{:{path_wid}} {:{desc_wid}} {}".format('Path/Key',
                                                                'Description',
                                                                'Tags', path_wid=path_col, desc_wid=desc_col))
    for secret in secrets:
        if secret.description:
            _desc = (secret.description[:28] + '..') if desc_col == 32 else secret.description
        else:
            _desc = 'None'
        _tags = json_to_tags(secret.tags) if secret.tags else 'None'
        print("{:{path_wid}} {:{desc_wid}} {}".format(secret.path,
                                                      _desc,
                                                      _tags, path_wid=path_col, desc_wid=desc_col))

def desc_col_length(secrets):
    """calculate width of DESCRIPTION column"""
    desc_vals = []
    for secret in secrets:
        if secret.description:
            desc_vals.append(len(secret.description))
    if not desc_vals or max(desc_vals) <= 16:
        desc_vals = [16]
    return 32 if max(desc_vals) >= 30 else max(desc_vals) + 2

def print_export(secrets, output='tfvars'):
    """export secret list in desired format"""
    options = {'tfvars': print_tfvars, 'json': print_json, 'csv': print_csv}
    if output in options:
        options[output]([secret.value for secret in secrets])
    else:
        print('secretctl: export format supported include tfvars, json, ')

def print_tfvars(secrets):
    """print key=value pairs to stdout"""
    for secret in secrets:
        for key in secret:
            print(f"{key}={secret[key]}")

def print_json(secrets):
    """print json formatted key: value pairs to stdout"""
    result = ""
    result += "{\n"
    for secret in secrets:
        for key in secret:
            result += f"\"{key}\": \"{secret[key]}\",\n"
    result = result[:-2] + "\n}"
    print(result)

def print_csv(secrets):
    """print csv formatted key,value pairs to stdout"""
    print('Key,Value')
    for secret in secrets:
        for key in secret:
            print(f"{key},{secret[key]}")
