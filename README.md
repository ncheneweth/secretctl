# secretctl
[![CirclecI][circle-badge]][circle-repo]
[![Test Coverage][cc-coverage-badge]][cc-coverage-repo]
[![Maintainability][cc-maintainability-badge]][cc-maintainability-repo]
[![License][license-badge]][license]
Command-line tool optimized for working with aws secrets manager in CI/CD pipelines.

[circle-badge]: https://circleci.com/gh/ncheneweth/secretctl.svg?style=svg
[circle-repo]: https://circleci.com/gh/ncheneweth/secretctl
[cc-coverage-badge]: https://api.codeclimate.com/v1/badges/01a1314e60921919bb12/test_coverage
[cc-coverage-repo]: https://codeclimate.com/github/ncheneweth/secretctl/test_coverage
[cc-maintainability-badge]: https://api.codeclimate.com/v1/badges/01a1314e60921919bb12/maintainability
[cc-maintainability-repo]: https://codeclimate.com/github/ncheneweth/secretctl/maintainability
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[license]: https://raw.githubusercontent.com/feedyard/circleci-base-agent/master/LICENSE

## Installing

## Usage

Commands:
  help      Show help.
  role      Define the IAM role to assume when accessing AWS.
  write     Write a secret.
  read      Read a secret.
  ls        List contents of a path.
  rm        Remove a secret or version.
  inspect   Print details of a resource.
  template  Inject secrets into a template.
  run       Pass secrets as environment variables to a process.


  is it needed?

  audit     Show the audit log.


  # local dev

GOOS = darwin, linux, windows
GOARCH = amd64, 386(win)
