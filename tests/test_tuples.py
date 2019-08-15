import json
import pytest
import boto3
from moto import mock_secretsmanager

from secretctl.tuples import get_secret
from secretctl.tuples import create_secret
from secretctl.tuples import update_secret
from secretctl.tuples import list_secrets

# moto does not support secretsmanager tag or untag tests

@mock_secretsmanager
def test_Secret():
    # fixtures
    fixture_value = "[{\"value_1\": \"abc123\"}]"
    fixture_value2 = "[{\"value_2\": \"abc123_2\"}]"
    secrets_created = ["myapp/dev/value_1", "myapp/dev/value_2"]
    fixture_updated_value = "[{\"value_1\": \"123abc\"}]"
    fixture_tags = [{ "Key": "value_1_tag", "Value": "value_1_tag_value" }]

    secret = create_secret('myapp/dev/value_1', fixture_value, description='fixture existing secret', tags=fixture_tags)
    assert secret.path == 'myapp/dev/value_1'

    # get: retrieve existing secret
    secret = get_secret('myapp/dev/value_1')
    assert secret.path == 'myapp/dev/value_1'
    assert secret.value == [{"value_1": "abc123"}]
    # moto does not support ['Description']
    # assert secret.description == 'fixture existing secret'
    assert secret.tags == [{ "Key": "value_1_tag", "Value": "value_1_tag_value" }]
    # moto does not support ['VersionIdsToStages']
    # assert secret.versions == 1

    # update existing secret and description
    secret = update_secret('myapp/dev/value_1', fixture_updated_value)
    secret = get_secret('myapp/dev/value_1')
    assert secret.path == 'myapp/dev/value_1'
    assert secret.value == [{"value_1": "123abc"}]
    # moto does not support ['Description']
    # assert secret.description == 'fixture existing secret'
    # moto update_secret bug: deletes tags
    # assert secret.tags == [{ "Key": "value_1_tag", "Value": "value_1_tag_value" }]
    # moto does not support ['VersionIdsToStages']
    # assert secret.versions == 1

    # fail: creating secret that already exists
    with pytest.raises(SystemExit):
        secret = create_secret('myapp/dev/value_1', '123abc')
        assert secret.value == '123abc'

    # list all secrets
    secret = create_secret('myapp/dev/value_2', fixture_value2, description='fixture existing secret 2', tags=fixture_tags)
    secrets = list_secrets()
    assert len(secrets) == 2
    for secret in secrets:
        assert secret['Name'] in secrets_created
