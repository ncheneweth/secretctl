package cmd

import (
	"fmt"

	// "github.com/spf13/cobra"
	//"reflect"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/credentials/stscreds"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
	"github.com/spf13/viper"
)

func newSecretsManagerSession() (svc *secretsmanager.SecretsManager) {
	sess := session.Must(session.NewSession())
	creds := credentials.NewEnvCredentials()

	if viper.GetString("AssumeRole") != "none" {
		creds = stscreds.NewCredentials(sess, viper.GetString("AssumeRole"))
	}
	_, err := creds.Get()
	if err != nil {
		fmt.Println("Error: can't retrieve ENV credentials")
		return
	}
	svc = secretsmanager.New(sess, &aws.Config{Credentials: creds})
	return svc
}
