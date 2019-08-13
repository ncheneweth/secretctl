from secretctl.cli import create, read_value, read, update, list, export
from secretctl.tuples import get_secret
from invoke import MockContext, Result
from moto import mock_secretsmanager
from io import StringIO
import pytest
import json

# test secretctl.cli.read_value()
def test_read_value():
    simple_value = 'abc123'
    json_value = "{\"key1\": \"value1\",\"key2\": \"value2\"}"
    malformed_json = "this is not a json string"

    assert read_value('app/env/value', simple_value, isjson=False) == "{\"value\": \"abc123\"}"
    assert read_value('0604a5a3-c5c5-49fb-aaa9-769cfadfb884/env/value', json_value, isjson=True) == json_value

    with pytest.raises(SystemExit):
        assert read_value('app/env/value', malformed_json, isjson=True) == {"value": "this is not a json string"}


@mock_secretsmanager
def test_cli(capsys, monkeypatch):
    _ctx = MockContext()
    json_value = """
    {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }\n
    """
    malformed_json = """
    {
        "key1": "value1"
        "key2": "value2"
        "key3": "value3"
    }\n
    """
    piped_input = StringIO(json_value)

    # test create cli with simple secret
    create(_ctx, 'app/env/val1', 'abc123', isjson=False, description=None, tags=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val1 created\n"
    secret = get_secret('app/env/val1')
    assert secret.path == 'app/env/val1'
    assert secret.value == {"val1": "abc123"}

    # test read cli of simple secret, --quiet --info
    read(_ctx, 'app/env/val1', quiet=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "abc123\n"
    read(_ctx, 'app/env/val1', quiet=False, info=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key        Version   Value
app/env/val1    1         abc123
*Desc                     No description
*Tags                     No tags
"""

    # test update cli with simple secret
    update(_ctx, 'app/env/val1', '123abc', isjson=False, description=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val1 updated\n"
    secret = get_secret('app/env/val1')
    assert secret.path == 'app/env/val1'
    assert secret.value == {"val1": "123abc"}

    # test create cli with piped input; '-'
    monkeypatch.setattr('sys.stdin', piped_input)
    create(_ctx, 'app/env/val2', '-', isjson=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val2 created\n"
    secret = get_secret('app/env/val2')
    assert secret.path == 'app/env/val2'
    assert secret.value == {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }

    # test read cli with json secret and --quiet
    read(_ctx, 'app/env/val2', quiet=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "value1\nvalue2\nvalue3\n"

    list(_ctx, path=None, tags=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key        Description        Tags
app/env/val1    None               None
app/env/val2    None               None
Found 2 secrets.
"""

    # test results from export, --tfvars --csv --json
    export(_ctx, 'app/', output='tfvars')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout =="""val1=123abc
key1=value1
key2=value2
key3=value3

"""

    export(_ctx, 'app/', output='csv')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout =="""Key,Value
val1,123abc
key1,value1
key2,value2
key3,value3

"""

    export(_ctx, 'app/', output='json')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout =="""{
"val1": "123abc",
"key1": "value1",
"key2": "value2",
"key3": "value3"
}
"""

    # test create cli fails on attempt to create existing secrets
    with pytest.raises(SystemExit):
        create(_ctx, 'app/env/val1', 'abc123', isjson=False, description=None, tags=None)

    # test create cli with malformed json
    piped_input = StringIO(malformed_json)
    with pytest.raises(SystemExit):
        monkeypatch.setattr('sys.stdin', piped_input)
        create(_ctx, 'app/env/val3', '-', isjson=True)

    # test read cli fails with secret not found
    with pytest.raises(SystemExit):
        read(_ctx, 'app/env/val3', quiet=True)

# for some reason testing two mocked user input behaviors in the same def fails?
@mock_secretsmanager
def test_update(capsys, monkeypatch):
    _ctx = MockContext()
    json_value = """
    {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }\n
    """
    piped_input = StringIO(json_value)

    create(_ctx, 'app/env/val1', 'abc123', isjson=False, description=None, tags=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val1 created\n"

    # test update cli with piped input; '-'
    monkeypatch.setattr('sys.stdin', piped_input)
    update(_ctx, 'app/env/val1', '-', isjson=True, description=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val1 updated\n"
    secret = get_secret('app/env/val1')
    assert secret.path == 'app/env/val1'
    assert secret.value == {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
