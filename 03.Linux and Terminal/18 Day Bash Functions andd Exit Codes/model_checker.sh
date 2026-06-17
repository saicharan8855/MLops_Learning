#!/bin/bash

MODELS=("iris_model.pkl" "spam_model.pkl" "price_model.pkl")

check_file() {
	local file=$1
	if [ -f "$file" ]; then
		echo "  FOUND: $file"
		return 0
	else
		echo "  MISSING: $file"
		return 1
	fi
}

echo "checking required model files ..."
echo ""


MISSING_COUNT=0

for model in "${MODELS[@]}"
do
	check_file "$model"
	if [ $? -ne 0 ]; then
		MISSING_COUNT=$((MISSING_COUNT + 1))
	fi
done

echo ""
echo "total missing: $MISSING_COUNT"

if [ $MISSING_COUNT -eq 0 ]; then
	echo "All models ready for deployement"
	exit 0
else
	echo "cannot diploy missing models"
	exit 1
fi
