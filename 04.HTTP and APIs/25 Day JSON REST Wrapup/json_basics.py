import json

# JSON object - single thing, key-value pairs
model_info = {
    "name": "iris-classifier",
    "version": "1.0",
    "accuracy": 0.95
}

# JSON array - list of things
all_models = [
    {"name": "iris-classifier", "version": "1.0"},
    {"name": "spam-detector", "version": "2.1"},
]

# convert Python dict/list to JSON string
print("Object as JSON string:")
print(json.dumps(model_info, indent=2))

print("")
print("Array as JSON string:")
print(json.dumps(all_models, indent=2))

# convert JSON string back to Python
json_string = '{"name": "fraud-detector", "version": "1.5"}'
parsed = json.loads(json_string)
print("")
print("Parsed back to Python dict:", parsed)
print("Type:", type(parsed))
