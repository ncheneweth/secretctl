package cmd

// secretctl default settings
const (
	// AssumeRole default define an AWS IAM role to assume
	AssumeRole = "none"

	ConfigEnvDefault             = "SECRETCTL"
	ConfigFileDefaultName        = "config"
	ConfigFileDefaultType        = "yaml"
	ConfigFileDefaultLocation    = "/.secretctl" // path will begin with $HOME dir
	ConfigFileDefaultLocationMsg = "config file (default is $HOME/.secretctl/config.yaml)"
)
