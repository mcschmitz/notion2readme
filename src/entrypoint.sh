#!/bin/bash

# Diagnostic output:
echo "Convert URL: $INPUT_URL"
echo '================================='

python main.py --token_v2 $TOKEN_V2 --url $INPUT_URL

echo '================================='
