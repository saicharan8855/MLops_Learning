#!/bin/bash


MODELS=("iris-classifier" "spam-detector" "price-predictor")


echo "all models: "
for model in "${MODELS[@]}"
do
	echo "  - $model"
done


echo ""
echo "First model : ${MODELS[0]}"

echo "total models : ${#MODELS[@]}"


MODELS+=("fraud-detector")
echo ""
echo "after adding one:"
for model in "${MODELS[@]}"
do
	echo "  - $model"
done
