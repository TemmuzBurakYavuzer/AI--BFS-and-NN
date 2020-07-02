
import pickle
import numpy as np
from keras.models import Sequential, load_model 
from keras.layers import Dense

f=open("train_data.txt", "rb")
train_data = pickle.load(f)
X = np.array([i[0] for i in train_data]).reshape(-1, 5)
Y = np.array([i[1] for i in train_data]).reshape(-1, 1)

model = Sequential()
model.add(Dense(25, input_dim=5, activation='relu'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam')

#model = load_model('my_model.h5')

model.fit(X, Y, epochs = 20, batch_size=128,  verbose=2)
model.save('my_model.h5')
