#!/bin/bash

echo "MLOps Model Runner"
echo "=================="


read -p "enter model name :" MODEL_NAME
read -p "enter version name :" VERSION
read -p "enter features (space seperated) : " FEATURES

echo ""
echo "running mdoel : $MODEL_NAME"
echo "version : $VERSION"
echo "features : $FEATURES"


read -p "Confirm ? (y/n) :" CONFIRM

if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
	echo "running prediction..."
	echo "done"
else
	echo "cancelled"
fi
