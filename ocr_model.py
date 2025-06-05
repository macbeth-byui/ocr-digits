import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle

'''
Create a model (ocr.mdl) using the training data (ocr.dat)
'''

# Load dataset
with open("ocr.dat","rb") as f:
    df = pickle.load(f)
feature_names = [f"b{i}" for i in range(100)]
target_names = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Split data into training and testing sets
x = df[feature_names]  # contains all of the column names that are inputs
y = df['target']       # contains the column name with the output

# Split: 80% train, 20% test (randomly selected) and Train a classifier
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

# Make predications and evaluate.  Use the 20% test data to see if succeeded.
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Generate and display the Confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=target_names)
cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)
print(cm_df)

# Save the model
with open("ocr.mdl", "wb") as f:
    pickle.dump(model, f)

