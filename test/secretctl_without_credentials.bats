#!/usr/bin/env bats

# no credentials provided

@test "evaluate ls" {
  run bash -c "secretctl ls"
  [[ "$output" =~ "KEY not found in environment" ]]
}
