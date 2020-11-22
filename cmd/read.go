package cmd

import (
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"runtime"
	"strconv"

	"github.com/atotto/clipboard"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
	"github.com/spf13/cobra"
)

// Clip -c : read secret into clipboard
var Clip bool

// Previous -p : return previous version of a secret
var Previous bool

// OutFile -o : write secret to Outfile
var OutFile string

// Mode -m : permission mode to apply to Outfile, default is 0600
var Mode string

// readCmd represents the read command
var readCmd = &cobra.Command{
	Use:   "read [<path>/<to>/...]<secret>",
	Short: "Read a secret.",
	Long:  `Read a secret.`,
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		var keyValue string
		version := "AWSCURRENT"
		if Previous {
			version = "AWSPREVIOUS"
		}
		keyValue = getSecret(args[0], version)

		if OutFile != "" {
			modeInt, err := strconv.ParseUint(Mode, 8, 32)
			check(err)
			fileMode := os.FileMode(modeInt)
			if !fileMode.IsRegular() {
				fmt.Println(fmt.Errorf("bad mode: %v", fileMode))
				return
			}
			err = ioutil.WriteFile(OutFile, []byte(keyValue), fileMode)
			check(err)
			fmt.Printf("Write %s to file.\n", args[0])
			cmd := exec.Command("ls", "-la", OutFile)
			if runtime.GOOS == "windows" {
				cmd = exec.Command("dir", OutFile)
			}
			cmd.Stdout = os.Stdout
			check(cmd.Run())
			return
		}
		if Clip {
			check(clipboard.WriteAll(keyValue))
			fmt.Printf("Copied %s to clipboard.\n", args[0])
			return
		}
		fmt.Println(keyValue)
	},
}

func init() {
	rootCmd.AddCommand(readCmd)

	readCmd.PersistentFlags().BoolVarP(&Clip, "clip", "c", false, "Copy the secret value to the clipboard.")
	readCmd.PersistentFlags().StringVarP(&OutFile, "out", "o", "", "Write the secret value to out=filename.")
	readCmd.PersistentFlags().StringVarP(&Mode, "mode", "m", "0600", "Set filemode for the output file.")
	readCmd.PersistentFlags().BoolVarP(&Previous, "previous", "p", false, "Read the previous version of the secret.")
}

func getSecret(keyName string, version string) (keyValue string) {
	svc := newSecretsManagerSession()
	input := &secretsmanager.GetSecretValueInput{
		SecretId:     aws.String(keyName),
		VersionStage: aws.String(version),
	}
	result, err := svc.GetSecretValue(input)
	if err != nil {
		if aerr, ok := err.(awserr.Error); ok {
			switch aerr.Code() {
			case secretsmanager.ErrCodeDecryptionFailure:
				// Secrets Manager can't decrypt the protected secret text using the provided KMS key.
				fmt.Println(secretsmanager.ErrCodeDecryptionFailure, aerr.Error())

			case secretsmanager.ErrCodeInternalServiceError:
				// An error occurred on the server side.
				fmt.Println(secretsmanager.ErrCodeInternalServiceError, aerr.Error())

			case secretsmanager.ErrCodeInvalidParameterException:
				// You provided an invalid value for a parameter.
				fmt.Println(secretsmanager.ErrCodeInvalidParameterException, aerr.Error())

			case secretsmanager.ErrCodeInvalidRequestException:
				// You provided a parameter value that is not valid for the current state of the resource.
				fmt.Println(secretsmanager.ErrCodeInvalidRequestException, aerr.Error())

			case secretsmanager.ErrCodeResourceNotFoundException:
				// We can't find the resource that you asked for.
				fmt.Println(secretsmanager.ErrCodeResourceNotFoundException, aerr.Error())
			}
		} else {
			// Print the error, cast err to awserr.Error to get the Code and
			// Message from an error.
			fmt.Println(err.Error())
		}
		return
	}
	if result.SecretString != nil {
		keyValue = *result.SecretString
	} else {
		fmt.Println("binary")
		decodedBinarySecretBytes := make([]byte, base64.StdEncoding.DecodedLen(len(result.SecretBinary)))
		len, err := base64.StdEncoding.Decode(decodedBinarySecretBytes, result.SecretBinary)
		if err != nil {
			fmt.Println("Base64 Decode Error:", err)
			return
		}
		keyValue = string(decodedBinarySecretBytes[:len])
	}

	return
}
