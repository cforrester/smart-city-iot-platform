import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

# Create dummy model
model = LogisticRegression()
X_train = np.array([[5.1, 3.5, 1.4, 0.2], [6.0, 3.0, 4.8, 1.8]])
y_train = np.array([0, 1])
model.fit(X_train, y_train)

# Save the model as model.pkl
joblib.dump(model, "model.pkl")
print("Dummy model saved as model.pkl")
