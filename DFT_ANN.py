# 01/05/2020
# Testing training with Keras API

from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import tensorflow as tf

# random seed for reproducibility
np.random.seed(7)
# print(np.__version__)

# loading the raag dataset
dataset = np.loadtxt("raag_dataset.csv", delimiter=',')
outputs = np.loadtxt("outputs.csv", delimiter=',')
# split into input (X) and output (Y) variables, splitting csv data

X = dataset[:, 0:2686764]
Y = outputs[:, 0:]
print("break point 1")


# create model, add dense layers one by one specifying activation function
model = Sequential()
model.add(Dense(22, input_dim=2686764, activation='relu'))
print("break point 2")
model.add(Dense(15, activation='relu'))
model.add(Dense(20, activation='relu'))
print("break point 3")
model.add(Dense(8, activation='relu'))
model.add(Dense(10, activation="relu"))
model.add(Dense(4, activation='sigmoid'))
print("break point 4")

# compile the model, adam gradient descent (optimized)
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
print("break point 5")
# call the function to fit to the dat (training the network)
model.fit(X, Y, epochs=200, batch_size=10)
print("break point 6")

# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %0.2f%%" %(model.metrics_names[1], scores[1]*100))
print("break point 7")

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

# importing a csv of a clip of Yemen Raag
testClip = np.loadtxt("C1_fmod.csv", delimiter=',')
print(np.shape(testClip))
print(type(testClip))

if testClip.ndim == 1:
    testClip = np.array([testClip])
    print(np.shape(testClip))
    print(type(testClip))

# make class predictions with the model
predictions = model.predict(testClip)
print(predictions)
print(np.shape(predictions))
print(type(predictions))
#
# # summarize the first 5 cases
# for i in range(5):
#     print('%d ' % (predictions[i]))

# (2686764,) but got array with shape (1,)


