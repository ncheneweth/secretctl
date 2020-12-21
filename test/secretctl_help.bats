#!/usr/bin/env bats

@test "general cli help" {
  run bash -c "secretctl"
  [ "${lines[0]}" = "pipeline optimized cli for use with aws secrets manager." ]
}

@test "inspect --help" {
  run bash -c "secretctl inspect --help"
  [ "${lines[0]}" = "Print detailed secret information." ]
}

@test "ls --help" {
  run bash -c "secretctl ls --help"
  [ "${lines[0]}" = "List contents of a path." ]
}

@test "read --help" {
  run bash -c "secretctl read --help"
  [ "${lines[0]}" = "Read a secret." ]
}

@test "rm --help" {
  run bash -c "secretctl rm --help"
  [ "${lines[0]}" = "Remove a directory or secret." ]
}

@test "role --help" {
  run bash -c "secretctl role --help"
  [ "${lines[0]}" = "Define an IAM role to assume when accessing AWS." ]
}

@test "shell --help" {
  run bash -c "secretctl shell --help"
  [ "${lines[0]}" = "Launch process with secrets as environment variables." ]
}

@test "template --help" {
  run bash -c "secretctl template --help"
  [ "${lines[0]}" = "Populate secrets in a template." ]
}

@test "write --help" {
  run bash -c "secretctl write --help"
  [ "${lines[0]}" = "Write a secret." ]
}
