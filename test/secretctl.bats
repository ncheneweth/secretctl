#!/usr/bin/env bats

# performs tests using AWS secrets manager for the account credentials provided
# see setup.sh for fixtures

@test "evaluate ls path" {
  run bash -c "secretctl ls test"
  [ "${lines[0]}" = "CREATED              NAME" ]
  [[ "${lines[1]}" =~ "test/secretctl/plain" ]]
  [[ "${lines[2]}" =~ "test/secretctl/json/single_key" ]]
  [[ "${lines[3]}" =~ "test/secretctl/json/multi_key" ]]
  [[ "${lines[4]}" =~ "test/secretctl/pem" ]]
}

@test "evaluate read plain" {
  run bash -c "secretctl read test/secretctl/plain"
  [ "$output" = "abc123xyz456" ]
}

@test "evaluate read single_key" {
  run bash -c "secretctl read test/secretctl/json/single_key"
  [ "$output" = "{\"user\":\"bob\"}" ]
}

@test "evaluate read multi_key" {
  run bash -c "secretctl read test/secretctl/json/multi_key"
  [ "$output" = "{\"user\":\"bob\",\"phrase\":\"abc123xyz456\"}" ]
}

@test "evaluate read pem" {
  run bash -c "secretctl read test/secretctl/pem"
  [ "${lines[0]}" = "-----BEGIN PUBLIC KEY-----" ]
  [ "${lines[1]}" = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsvX9P58JFxEs5C+L+H7W" ]
  [ "${lines[7]}" = "DQIDAQAB" ]
  [ "${lines[8]}" = "-----END PUBLIC KEY-----" ]
}
