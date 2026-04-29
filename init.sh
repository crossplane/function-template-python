#!/bin/sh

# This script helps initialize a new function project by
# replacing all instances of function-template-python with the
# name of your function. The script accepts two arguments:
# 1. The name of your function
# 2. The path to your function directory

set -e

cd "$2" || return

# Replace function-template-python with the name of your function
# in package/crossplane.yaml
perl -pi -e s,function-template-python,"$1",g package/crossplane.yaml
# in example YAML files
find example -type f -print0 | xargs -0 -I {} perl -pi -e s,function-template-python,"$1",g {}

echo "Function $1 has been initialized successfully"
