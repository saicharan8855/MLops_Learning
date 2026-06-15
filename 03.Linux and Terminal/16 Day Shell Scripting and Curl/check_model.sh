#!/bin/bash

MODEL_FILE="iris_model.pkl"

if [ -f "$MODEL_FILE" ]; then
	echo "model file found : $MODEL_FILE"
else
	echo "model file not found : $MODEL_FILE"
	echo "please train the model first"
fi
