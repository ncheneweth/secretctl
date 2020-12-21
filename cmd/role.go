package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var roleCmd = &cobra.Command{
	Use:   "role",
	Short: "Define an IAM role to assume when accessing AWS.",
	Long:  `Define an IAM role to assume when accessing AWS.`,
}

func init() {
	rootCmd.AddCommand(roleCmd)
	roleCmd.AddCommand(showCmd)
	roleCmd.AddCommand(setCmd)
	roleCmd.AddCommand(unsetCmd)
}

// display current secretctl configuration
var showCmd = &cobra.Command{
	Use:   "show",
	Short: "Show current Role ARN.",
	Long:  `Show current Role ARN.`,
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		for _, s := range viper.AllKeys() {
			fmt.Printf("%s: %s\n", s, viper.GetString(s))
		}
	},
}

// set the current secretctl role configuration
var setCmd = &cobra.Command{
	Use:   "set ARN",
	Short: "set the IAM RoleARN to assume.",
	Long:  `set the IAM RoleARN to assume.`,
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		viper.Set("AssumeRole", args[0])
		exitError(viper.WriteConfigAs(viper.ConfigFileUsed()))
		fmt.Printf("set assumerole: %s\n", args[0])
	},
}

// clear the current secretctl role configuration
var unsetCmd = &cobra.Command{
	Use:   "unset",
	Short: "Clear the IAM RoleARN.",
	Long:  `Clear the IAM RoleARN.`,
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		exitError(os.Remove(viper.ConfigFileUsed()))
		fmt.Println("Role ARN setting reset to default")
	},
}
