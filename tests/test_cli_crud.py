from moto import mock_secretsmanager
from invoke import MockContext
from io import StringIO
import pytest

from secretctl.cli import create
from secretctl.cli import read
from secretctl.cli import update

@mock_secretsmanager
def test_create_read_update_delete(capsys, monkeypatch):
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

    # test create cli with piped input; '-'
    monkeypatch.setattr('sys.stdin', piped_input)
    create(_ctx, 'app/env/val2', '-', isjson=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val2 created\n"

    # test read cli of simple secret, --quiet
    read(_ctx, 'app/env/val1', quiet=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "abc123\n"

    # test read cli of json value, --quiet
    read(_ctx, 'app/env/val2', quiet=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "value1\nvalue2\nvalue3\n"

    # test update cli with simple secret
    update(_ctx, 'app/env/val1', '123abc', isjson=False, description=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "app/env/val1 updated\n"

    # confirm outcome of update
    read(_ctx, 'app/env/val1', quiet=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == "123abc\n"

    # moto does not yet support description or tag resources for sercretsemanager

    # test create cli fails on attempt to create existing secrets
    with pytest.raises(SystemExit):
        create(_ctx, 'app/env/val1', 'new abc123', isjson=False, description=None, tags=None)

    # test read cli fails on attempt to read nonexisting secret
    with pytest.raises(SystemExit):
        read(_ctx, 'app/env/val3', quiet=True)

    # test update cli fails on attempt to update nonexisting secret
    with pytest.raises(SystemExit):
        update(_ctx, 'app/env/val3', '123abc', isjson=False, description=None)
