#!/bin/bash

echo "----****----"
echo "iris mlops pipeline"
echo "----****----"

MODEL_PATH="iris_model.pkl"
if [ -f " $MODEL_PATH" ]; then
	echo "model already exists - skipping training"
else 
	echo "model not found - training now"
	echo "training complete"
	touch $MODEL_PATH
fi

LOG_FILE="pipeline.log"
echo "pipeline ran at : $(date)" >> $LOG_FILE
echo "model path : $MODEL_PATH" >> $LOGFILE


echo ""
echo "log saved to $LOG_FILE"
cat $LOG_FILE
