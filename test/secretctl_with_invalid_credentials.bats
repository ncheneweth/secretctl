#!/usr/bin/env bats

# invalid credentials provided

@test "evaluate ls" {
  run bash -c "secretctl ls"
  [ "$output" = "The security token included in the request is invalid." ]
}
