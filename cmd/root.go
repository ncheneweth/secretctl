package cmd

import (
	"fmt"
	"os"
	homedir "github.com/mitchellh/go-homedir"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "secretctl",
	Short: "multisource secrets management",
	Long: `pipeline optimized cli for use with aws secrets manager.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	// Run: func(cmd *cobra.Command, args []string) { },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

  rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", ConfigFileDefaultLocationMsg)
}

// initConfig sets the config values based on the following order of precedent:
// ENV variables
// Config file definitions
// Default values from constant.go
func initConfig() {
	viper.SetDefault("AssumeRole", AssumeRole)

	viper.SetEnvPrefix(ConfigEnvDefault)
	viper.AutomaticEnv()

	if cfgFile != "" {
		// Use config file from the flag.
		viper.SetConfigFile(cfgFile)
	} else {
    viper.AddConfigPath(defaultConfigLocation())
    viper.SetConfigName(ConfigFileDefaultName)
	}

	// If a config file is found, read it in, else write a blank.
  if err := viper.ReadInConfig(); err != nil {
		home := defaultConfigLocation()

		check(os.MkdirAll(home, 0700))
    fmt.Println(home+"/"+ConfigFileDefaultName+"."+ConfigFileDefaultType)
    emptyFile, err := os.Create(home+"/"+ConfigFileDefaultName+"."+ConfigFileDefaultType)
  	check(err)
  	emptyFile.Close()
  }
}

func defaultConfigLocation() string {
  home, err := homedir.Dir()
  check(err)
  return home + ConfigFileDefaultLocation
}

func check(e error) {
	if e != nil {
			panic(e)
	}
}
