import pickle
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 


iris = load_iris() 
X , y = iris.data , iris.target 

X_train , X_test , y_train , y_test = train_test_split(
    X , y , test_size = 0.2 , random_state = 42
)

model = RandomForestClassifier(
    n_estimators = 100 , random_state = 42
)
model.fit(X_train , y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test , predictions)
print(f"Accuracy: {accuracy:.2f}")

os.makedirs("model" , exist_ok = True) 
with open("model/iris_model.pkl" , "wb") as f:
    pickle.dump(model , f) 
print("model saved to model/iris_model.pkl")

print(f"Classes: {list(iris.target_names)}")