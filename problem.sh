#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <problemName>"
	exit 1
fi

problem=$(echo "$1" | tr ' ' '_' | tr -cd '[:alnum:]_')

if [[ -z "$problem" ]]; then
    echo "Problem name must contain at least one alphanumeric character"
    exit 1
fi

if [[ "$problem" == *.* ]]; then
	echo "Problem name cannot contain an extension"
	exit 1
fi

if [[ -d "Problems/$problem" ]]; then
	echo "Problem folder already exists"
	exit 1
fi

mkdir -p "Problems/$problem"
cp template.cpp "Problems/$problem/$problem.cpp"

echo "Problems/$problem" >> problemList.txt
