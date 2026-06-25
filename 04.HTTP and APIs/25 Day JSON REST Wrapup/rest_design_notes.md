# REST API Design — Iris Model Service

## Bad design (verb-based, not RESTful)
GET  /getAllModels
GET  /getModelById?id=5
POST /createNewPrediction
POST /deleteModel?id=5

## Good design (resource-based, RESTful)
GET    /models              → list all models
GET    /models/5            → get model with id 5
POST   /models               → create a new model
DELETE /models/5             → delete model with id 5

GET    /models/5/predictions       → all predictions made by model 5
POST   /predictions                → create a new prediction
GET    /predictions/123            → get a specific prediction result

## The pattern
- URL = WHAT (the resource/noun)
- HTTP method = HOW (the action/verb)

Same URL, different method = different meaning:
GET    /models/5   → fetch model 5
DELETE /models/5   → delete model 5
PUT    /models/5   → replace model 5 entirely
