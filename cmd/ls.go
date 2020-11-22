package cmd

import (
	"fmt"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
	"github.com/spf13/cobra"
	"strings"
)

// list all secrets on path, no path means all
var lsCmd = &cobra.Command{
	Use:   "ls [path]",
	Short: "List contents of a path.",
	Long:  `List contents of a path.`,
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		svc := newSecretsManagerSession()

		input := &secretsmanager.ListSecretsInput{}
		err := svc.ListSecretsPages(input,
			func(page *secretsmanager.ListSecretsOutput, lastPage bool) bool {
				fmt.Printf("%-20s NAME\n", "CREATED")
				for key := 0; key < len(page.SecretList); key++ {
					if len(args) == 1 {
						if strings.Contains(*(page.SecretList[key].Name), args[0]) {
							fmt.Printf("%v  %s\n", (page.SecretList[key].CreatedDate).Format("2006-01-02 15:04:05"), *(page.SecretList[key].Name))
						}
					} else {
						fmt.Printf("%v  %s\n", (page.SecretList[key].CreatedDate).Format("2006-01-02 15:04:05"), *(page.SecretList[key].Name))
					}
				}
				return true
			})
		if err != nil {
			fmt.Println("Error: can't list secrets")
			return
		}

	},
}

func init() {
	rootCmd.AddCommand(lsCmd)
}
