package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// templateCmd represents the template command
var templateCmd = &cobra.Command{
	Use:   "template",
	Short: "Populate secrets in a template.",
	Long:  `Populate secrets in a template.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("template called")
	},
}

func init() {
	rootCmd.AddCommand(templateCmd)
}
