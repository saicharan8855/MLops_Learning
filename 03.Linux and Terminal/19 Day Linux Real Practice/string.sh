#!/bin/bash

MODEL="iris-classifier-v1.0"


echo "length : ${#MODEL}"

echo "Uppercase : ${MODEL^^}"

echo "lowercase : ${MODEL,,}"

echo "replace : ${MODEL/iris/flower}"

echo "first 4 chars : ${MODEL:0:4}"

if [[ "$MODEL" == *"iris"* ]]; then
	echo "model name contains ' iris'"
fi


if [[ "$MODEL" == iris* ]]; then
	echo "model name starts with 'iris' "
fi 

