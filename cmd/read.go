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
			exitError(err)
			fileMode := os.FileMode(modeInt)
			if !fileMode.IsRegular() {
				fmt.Println(fmt.Errorf("bad mode: %v", fileMode))
				return
			}
			err = ioutil.WriteFile(OutFile, []byte(keyValue), fileMode)
			exitError(err)
			fmt.Printf("Write %s to file.\n", args[0])
			cmd := exec.Command("ls", "-la", OutFile)
			if runtime.GOOS == "windows" {
				cmd = exec.Command("dir", OutFile)
			}
			cmd.Stdout = os.Stdout
			exitError(cmd.Run())
			return
		}

		if Clip {
			exitError(clipboard.WriteAll(keyValue))
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
	exitError(err)

	if result.SecretString != nil {
		keyValue = *result.SecretString
	} else {
		fmt.Println("binary")
		decodedBinarySecretBytes := make([]byte, base64.StdEncoding.DecodedLen(len(result.SecretBinary)))
		len, err := base64.StdEncoding.Decode(decodedBinarySecretBytes, result.SecretBinary)
		exitError(err)
		keyValue = string(decodedBinarySecretBytes[:len])
	}
	return
}
