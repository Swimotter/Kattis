#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <problemName>"
	exit 1
fi

python test.py $1 Problems problems.yaml
