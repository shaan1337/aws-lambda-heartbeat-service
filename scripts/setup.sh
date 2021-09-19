#!/usr/bin/env bash
SCRIPT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd "${SCRIPT_ROOT}/../" &>/dev/null

mkdir -p libs

pushd libs &> /dev/null
pip3 install boto3 --target .
popd libs &> /dev/null

popd &>/dev/null
