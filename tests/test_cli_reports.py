from moto import mock_secretsmanager
from invoke import MockContext
from io import StringIO
import pytest

from secretctl.cli import read
from secretctl.cli import create
from secretctl.cli import list
from secretctl.cli import export
from secretctl.cli import tag
from secretctl.cli import untag

@mock_secretsmanager
def test_formatted_output(capsys, monkeypatch):
    _ctx = MockContext()

    # reporting fixtures
    fixtures = [
        {"path": "app/dev/secret1", "value": "111", "tags": "team=one"},
        {"path": "app/dev/secret2", "value": "222", "tags": "team=two"},
        {"path": "app/qa/secret3", "value": "333", "tags": "team=three"}
    ]
    json_value = """
    {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }\n
    """
    piped_input = StringIO(json_value)
    for secret in fixtures:
        create(_ctx, secret['path'], secret['value'], isjson=False, description=None, tags=secret['tags'])
        captured_stdout, captured_stderr = capsys.readouterr()
    monkeypatch.setattr('sys.stdin', piped_input)
    create(_ctx, 'app/qa/secret4', '-', isjson=True)
    captured_stdout, captured_stderr = capsys.readouterr()

    # test read cli --info output formatting
    read(_ctx, 'app/dev/secret1', quiet=False, info=True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key           Version   Value
app/dev/secret1    1         111
*Desc                        No description
*Tags                        team=one
"""

    # test read cli multi-key (json) formatting
    read(_ctx, 'app/qa/secret4', quiet=False, info=False)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key          Version   Value
app/qa/secret4    1         {"key1": "value1", "key2": "value2", "key3": "value3"}
"""

    # test list cli, no path or tag filter
    list(_ctx, path=None, tags=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key           Description        Tags
app/dev/secret1    None               team=one
app/dev/secret2    None               team=two
app/qa/secret3     None               team=three
app/qa/secret4     None               None
Found 4 secrets.
"""

    # test list cli, --path but no tag filter
    list(_ctx, path='app/dev', tags=None)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key           Description        Tags
app/dev/secret1    None               team=one
app/dev/secret2    None               team=two
Found 2 secrets.
"""

    # test list cli, no path but with tag filter
    list(_ctx, path=None, tags='one')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout == """\x1b[33mPath/Key           Description        Tags
app/dev/secret1    None               team=one
Found 1 secrets.
"""

    # test results from export, --tfvars
    export(_ctx, 'app/', output='tfvars')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout =="""secret1=111
secret2=222
secret3=333
key1=value1
key2=value2
key3=value3
"""

    # test results from export, --csv
    export(_ctx, 'app/', output='csv')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout =="""Key,Value
secret1,111
secret2,222
secret3,333
key1,value1
key2,value2
key3,value3
"""

    # test results from export, --json
    export(_ctx, 'app/', output='json')
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout =="""{
"secret1": "111",
"secret2": "222",
"secret3": "333",
"key1": "value1",
"key2": "value2",
"key3": "value3"
}
"""
