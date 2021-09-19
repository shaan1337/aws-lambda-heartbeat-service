#!/usr/bin/env bash
SCRIPT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd "${SCRIPT_ROOT}/../" &>/dev/null

rm package.zip || true &> /dev/null

pushd libs &>/dev/null
zip -r9 ../package.zip .
popd &>/dev/null

zip -g package.zip *.py
echo
echo "Deploying to AWS Lambda..."
aws lambda update-function-code --function-name $1 --zip-file fileb://package.zip

popd &>/dev/null