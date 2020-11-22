package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// writeCmd represents the write command
var writeCmd = &cobra.Command{
	Use:   "write <path>[/<to> ...]/<secret>",
	Short: "Write a secret.",
	Long:  `Write a secret.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("write called")
	},
}

func init() {
	rootCmd.AddCommand(writeCmd)
}
