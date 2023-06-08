#!/bin/bash

set -e
set -u

VARIANT=${1:-}

case "$VARIANT" in
    cpu|nvidia)
    ;;
    *) 
        echo "Invalid variant '$VARIANT'. Only 'cpu' and 'nvidia' are supported."
        echo "Usage:"
        echo "docker/build.sh {cpu|nvidia}"
        exit 1
    ;;
esac

cd "$(dirname $0)"

echo "# This file is autogenerated! Do not edit!" > Dockerfile.generated
cat Dockerfile.$VARIANT >> Dockerfile.generated
cat Dockerfile.common >> Dockerfile.generated

docker build -t "roop-$VARIANT" -f "Dockerfile.generated" ..
