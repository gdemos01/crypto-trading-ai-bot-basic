import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
import numpy as np
from sklearn.metrics import  f1_score, accuracy_score

class Model:

    def __init__(self,model_name,x_train):
        self.model_name = model_name
        self.model = self.buildModel(x_train)
        print("> New model initialized: ",model_name)


    def buildModel(self,x_train):
        model = Sequential()
        x = len(x_train[0])

        model.add(LSTM(256,input_shape=((1,x)), return_sequences = True, activation = "relu"))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add(LSTM(128, input_shape=((1, x)), return_sequences=True, activation="relu"))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add(LSTM(128, input_shape=((1, x)), activation="relu"))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())

        model.add(Dense(32, activation="relu"))
        model.add(Dropout(0.2))

        model.add(Dense(2, activation="softmax"))
        optimizer = tf.keras.optimizers.Adam(lr = 0.001, decay = 1e-6)
        model.compile(loss="sparse_categorical_crossentropy",optimizer=optimizer)

        return model

    def train(self,x_train,y_train, batch_size, epochs):
        x_train = x_train.reshape(-1,1,len(x_train[0]))
        print("> Training model - ",self.model_name)
        self.model.fit(x_train,y_train,batch_size = batch_size, epochs = epochs)

    def evaluate(self,x_test,y_test):
        x_test = x_test.reshape(-1,1,len(x_test[0]))
        print("> Evaluating model - ",self.model_name)
        predictions = np.array(tf.argmax(self.model.predict(x_test),1))

        expected_increase = 0
        found_increase = 0
        expected_decrese = 0
        found_decrese = 0

        for i in range(0,len(predictions)):
            if y_test[i] == 0:
                expected_decrese += 1
                if predictions[i] == y_test[i]:
                    found_decrese += 1
            else:
                expected_increase += 1
                if predictions[i] == y_test[i]:
                    found_increase += 1

        accuracy = accuracy_score(y_test,predictions)
        print(">> Accuracy: ",accuracy)
        print(">> Increase Acc: ",(found_increase/expected_increase)," Decrese Acc: ",(found_decrese/expected_decrese))
        #loss = self.model.evaluate(x_test,y_test)
        #print("Loss re: ",loss)

    def predict(self,sample):
        sample = sample.reshape(-1, 1, len(sample[0]))
        prediction = np.array(tf.argmax(self.model.predict(sample),1))[0]

        return prediction