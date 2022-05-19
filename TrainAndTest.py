from modules import *
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class TrainAndTest:
    def __init__(self):
        self.data = DataLoader.Data()
        self.target = ['vote_average']
        self.features = list(self.data.movies.columns)
        self.features.remove(self.target[0])
        # set predictors' (X) and tagret (y) values
        self.X = self.data.movies[self.features]
        self.y = self.data.movies[self.target]
        # standardize data
        self.PredictorScaler = StandardScaler()
        self.TargetVarScaler = StandardScaler()
        # create fit object
        self.PredictorScalerFit = self.PredictorScaler.fit(self.X)
        self.TargetVarScalerFit = self.TargetVarScaler.fit(self.y)
        # generate standardized values of reatures and target
        self.X = self.PredictorScalerFit.transform(self.X)
        self.y = self.TargetVarScalerFit.transform(self.y)
        # split data into train and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=123)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # print(self.X_train.shape)
        # print(self.y_train.shape)
        # print(self.X_test.shape)
        # print(self.y_test.shape)




