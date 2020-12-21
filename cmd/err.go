package cmd

import (
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go/aws/awserr"
)

func exitError(err error) bool {
	if err != nil {
		if awsErr, ok := err.(awserr.Error); ok {
			fmt.Println(awsErr.Message())
			os.Exit(1)
		}
	}
	return true
}
