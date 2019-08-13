"""cli output formatters"""
import sys
import json
from secretctl.validators import json_to_tags
from colorama import init, Fore
init(autoreset=True)

# print formatted results of read to stdout
def print_read(secret, quiet=False, info=False):
    """format secretctl read response"""
    if quiet:
        for _key, value in secret.value.items():
            print(value)
    else:
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
    resp = ""
    if output == 'csv': resp+="Key,Value\n"
    if output == 'json': resp+="{\n"
    for index, secret in enumerate(secrets):
        for key, value in secret.value.items():
            if output == 'tfvars':
                resp+=f"{key}={value}\n"
            elif output == 'json':
                resp+=f"\"{key}\": \"{value}\",\n"
            elif output == 'csv':
                resp+=f"{key},{value}\n"
            else:
                print('secretctl: supported export formats json, csv, tfvars(default)')
                sys.exit(1)
    if output == 'json': resp = resp[:-2] + "\n}"
    print(resp)
