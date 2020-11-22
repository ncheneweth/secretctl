package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// inspectCmd represents the inspect command
var inspectCmd = &cobra.Command{
	Use:   "inspect <path>[/<to> ...]/<secret>",
	Short: "Print detailed secret information.",
	Long: `Print detailed secret information.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("inspect called")
	},
}

func init() {
	rootCmd.AddCommand(inspectCmd)
}
