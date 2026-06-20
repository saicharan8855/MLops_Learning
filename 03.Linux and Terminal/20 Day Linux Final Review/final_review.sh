#!/bin/bash


# linux final week review script

LOG_FILE="review.log"
DATA_FILE="sample_data.txt"


log() {
	local message=$1
	echo "$(date '+%H:%M:%S') - $message" | tee -a $LOG_FILE
}


# sample data

log "Creating sample data..."
echo "model,accuracy,version" > $DATA_FILE
echo "iris-classifier,0.95,1.0" >> $DATA_FILE
echo "spam_detector,0.89,1.0" >> $DATA_FILE
echo "price-predictor,0.76,2.0" >> $DATA_FILE
echo "fraud-detector,0.92,1.0" >> $DATA_FILE


log "Sample data created"
echo ""


# read and display
echo "--- full data ---"
cat $DATA_FILE
echo ""


# search with grep
echo "--- mdoels with accurqcy above 0.9 ---"
grep -E "0\.9[0-9]" $DATA_FILE
echo ""


# part 4 - count lines

TOTAL=$(wc -l < $DATA_FILE)
log "Total lines in data file: $TOTAL"
echo ""

# loop through and check each model 
echo "-- checking each model --"
MODELS=("iris-classifier" "spam-detector" "price-predictor" "fraud-detector")

for model in "${MODELS[@]}"
do
	if grep -q "$model" "$DATA_FILE"; then
		log "Verified : $model exists in data"
	else 
		log "missing : $model not found"
	fi
done
echo ""

# environment check
echo "--- environment check"
log "user : $USER"
log "home : $HOME"
log "current dir : $(pwd)"
echo ""

# cleanup with confirmation
read -p "delete log and data files? (y/n) : " CONFIRM
if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
	rm $DATA_FILE
	log "cleanup complete"
else
	log "cleanup skipped"
fi

echo ""
echo "review script complete!"
