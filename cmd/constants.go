package cmd

const (
	AssumeRole = "none"

  ConfigEnvDefault = "SECRETCTL"
  ConfigFileDefaultName = "config"
	ConfigFileDefaultType = "yaml"
	ConfigFileDefaultLocation = "/.secretctl"  // path will begin with $HOME dir
  ConfigFileDefaultLocationMsg = "config file (default is $HOME/.secretctl/config.yaml)"
)
