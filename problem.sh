#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <problemName>"
    exit 1
fi

problem="$1"

if [[ "$problem" == *.* ]]; then
    echo "Problem name cannot contain an extension"
    exit 1
fi

mkdir -p "Problems/$1"
cp template.cpp "Problems/$1/$1.cpp"
