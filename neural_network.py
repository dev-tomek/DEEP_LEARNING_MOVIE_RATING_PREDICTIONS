from modules import *
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import Sequential
from keras.layers import Dense

class NeuralNetwork:
    def __init__(self):
        self.train_test = TrainAndTest.TrainAndTest()
        # create ANN sequential model
        self.model = Sequential()
        # input layer and first hidden layer 
        self.n_features = len(self.train_test.features)
        # 82 features -> 82 input neurons -> 1 output neuron -> 82 x 2/3 + 1
        self.model.add(Dense(units = 55, input_dim=self.n_features, kernel_initializer='normal', activation='relu'))
        # second hidden layer
        self.model.add(Dense(units = 55, kernel_initializer = 'normal', activation = 'relu'))
        # output layer
        self.model.add(Dense(units = 1, kernel_initializer = 'normal'))
        # compile the model
        self.model.compile(loss = 'mean_squared_error', optimizer = 'adam') 
        # fit the ANN model
        self.model.fit(self.train_test.X_train, self.train_test.y_train, validation_split=0.33, batch_size = 32, epochs = 10, verbose = 1) 
        self.user_row = self.train_test.user_row
        self.p = self.prediction_constraint()

    def prediction_constraint(self):
        if self.user_row is None:
            p = None
        else:
            p = self.prediction()
        return p 
        

    def prediction(self):
        print(type(self.train_test.X_test))
        print(np.reshape(self.user_row, (1, 82)).shape)
        print(np.reshape(self.user_row, (1, 82)))
        p = self.model.predict(np.reshape(self.user_row, (1, 82)))
        p = self.train_test.TargetVarScalerFit.inverse_transform(p)
        return p

        # self.predictions = self.model.predict(self.train_test.X_test)
        # self.predictions = self.train_test.TargetVarScalerFit.inverse_transform(self.predictions)
        # # Scaling the y_test Price data back to original price scale
        # self.y_test_orig = self.train_test.TargetVarScalerFit.inverse_transform(self.train_test.y_test)
        # self.Test_Data = self.train_test.PredictorScalerFit.inverse_transform(self.train_test.X_test)

        # self.TestingData = pd.DataFrame(data=self.Test_Data, columns=self.train_test.features)
        # self.TestingData['VoteAverage'] = self.y_test_orig
        # self.TestingData['PredictedVote'] = self.predictions
        # print(self.TestingData.head(20))

        # # Mean Absolute Percentage Error
        # self.mape = np.mean(100 * (np.abs(self.TestingData['VoteAverage'] - self.TestingData['PredictedVote'])/self.TestingData['VoteAverage']))
        # print("Accuracy: " + str(100 - self.mape))
