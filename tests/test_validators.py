import pytest
from secretctl.validators import validate_path, validate_recovery, tags_to_json, read_value
import sys

# test secretctl.validators.validate_path()
def test_validate_path():
    # confirm valid path names
    assert validate_path('app/env/value') == 'app/env/value'
    assert validate_path('teams/team-name/service-name/env/secret.value') == 'teams/team-name/service-name/env/secret.value'
    assert validate_path('0604a5a3-c5c5-49fb-aaa9-769cfadfb884/env/value') == '0604a5a3-c5c5-49fb-aaa9-769cfadfb884/env/value'

    # length < 3
    with pytest.raises(SystemExit):
        assert validate_path('a') == 'a'

    # length > 256
    with pytest.raises(SystemExit):
        assert validate_path('a' * 257) == 'a' * 257

    # invalid characters
    with pytest.raises(SystemExit):
        assert validate_path('app:env') == 'app:env'
    with pytest.raises(SystemExit):
        assert validate_path('app/env/name with spaces') == 'app/env/name with spaces'

# test secretctl.validators.validate_recovery()
def test_validate_recovery():
    assert validate_recovery('14') == '14'

    # length not in 1..180 range
    with pytest.raises(SystemExit):
        assert validate_recovery('200') == '200'

# test secretctl.validators.tags_to_json()
def test_tags_to_json():
    # confirm valid tags
    assert tags_to_json('tag=value') == [{"Key": "tag", "Value": "value"}]
    assert tags_to_json('tag1 = value1 , tag2= value2') == [{"Key": "tag1", "Value": "value1"}, {"Key": "tag2", "Value": "value2"}]
    assert tags_to_json('  tag= value') == [{"Key": "tag", "Value": "value"}]
    assert tags_to_json('tag.id=0604a5a3-c5c5-49fb-aaa9-769cfadfb884') == [{"Key": "tag.id", "Value": "0604a5a3-c5c5-49fb-aaa9-769cfadfb884"}]

    assert tags_to_json('tag1, tag2', novalue=True) == ["tag1", "tag2"]

    # invalid characters
    with pytest.raises(SystemExit):
        assert tags_to_json('tag=va lue') == "[{\"Key\": \"tag\", \"Value\": \"va lue\"}]"
    with pytest.raises(SystemExit):
        assert tags_to_json('tag=va!ue') == "[{\"Key\": \"tag\", \"Value\": \"va!ue\"}]"
    with pytest.raises(SystemExit):
        assert tags_to_json('tag1, ta g2', novalue=True) == ["tag1", "tag2"]

    # not a comma delimited list
    with pytest.raises(SystemExit):
        assert tags_to_json('tag1 = value1 tag2= value2') == "[{\"Key\": \"tag1\", \"Value\": \"value1\"}, {\"Key\": \"tag2\", \"Value\": \"value2\"}]"
    with pytest.raises(SystemExit):
        assert tags_to_json('tag1 tag2', novalue=True) == ["tag1", "tag2"]

# test secretctl.validators.json_to_tags()
def json_to_tags():
    # confirm valid transformation - can assume will always receive valid json from secretsmanager
    assert json_to_tags({"Key": "tag", "Value": "value"}) == 'tag=value'
    assert json_to_tags({"Key": "tag1", "Value": "value1"}, {"Key": "tag2", "Value": "value2"}) == 'tag1=value1, tag2=value2'


# test secretctl.cli.read_value()
def test_read_value():
    simple_value = 'abc123'
    json_value = "{\"key1\": \"value1\",\"key2\": \"value2\"}"
    malformed_json = "this is not a json string"

    assert read_value('app/env/value', simple_value, isjson=False) == "{\"value\": \"abc123\"}"
    assert read_value('0604a5a3-c5c5-49fb-aaa9-769cfadfb884/env/value', json_value, isjson=True) == json_value

    with pytest.raises(SystemExit):
        assert read_value('app/env/value', malformed_json, isjson=True) == {"value": "this is not a json string"}
