# secretctl
[![CirclecI][circle-badge]][circle-repo]
[![Test Coverage][cc-coverage-badge]][cc-coverage-repo]
[![Maintainability][cc-maintainability-badge]][cc-maintainability-repo]
[![License][license-badge]][license]
Command-line tool for working with aws secrets manager.

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

Management Commands:
  credentials Manage your credentials.
  config      Manage your local configuration.

Commands:
  help      Show help.
  init      Initialize the secretctl client for first use on this device.
  write     Write a secret.
  read      Read a secret.
  generate  Generate a random secret.
  ls        List contents of a path.
  rm        Remove a directory, secret or version.
  tree      List contents of a directory in a tree-like format.
  inspect   Print details of a resource.
  template  Inject secrets into a template.
  run       Pass secrets as environment variables to a process.


  is it needed?
  mkdir     Create a new directory.
  audit     Show the audit log.