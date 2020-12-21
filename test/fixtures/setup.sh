#!/usr/bin/env bash
set -e

PLAIN="abc123xyz456"
SINGLE_KEY_VALUE_PAIR="{\"user\":\"bob\"}"
MULTI_KEY_VALUE_PAIRS="{\"user\":\"bob\",\"phrase\":\"abc123xyz456\"}"

aws secretsmanager create-secret --name "test/secretctl/plain" --secret-string $PLAIN > results.log
aws secretsmanager create-secret --name "test/secretctl/json/single_key" --secret-string $SINGLE_KEY_VALUE_PAIR >> results.log
aws secretsmanager create-secret --name "test/secretctl/json/multi_key" --secret-string $MULTI_KEY_VALUE_PAIRS >> results.log
aws secretsmanager create-secret --name "test/secretctl/pem" --secret-string file://public.key >> results.log
