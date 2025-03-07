import tensorflow as tf
import numpy as np

# Create synthetic training data
X_train = np.array([[5.1, 3.5, 1.4, 0.2], [6.0, 3.0, 4.8, 1.8], [5.8, 2.7, 5.1, 1.9]])
y_train = np.array([0, 1, 1])  # Labels (e.g., 0 = Setosa, 1 = Versicolor)

# Define a simple neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(4,)),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(2, activation="softmax")  # Assuming binary classification
])

# Compile model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train model
model.fit(X_train, y_train, epochs=10, verbose=1)

# Save model in TensorFlow SavedModel format
model.save("model.keras")
print(" Model saved successfully!")
