from modules import *
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class TrainAndTest:
    def __init__(self):
        self.data = DataLoader.Data()
        #input row placeholder
        self.input_row = None
        self.target = ['vote_average']
        self.features = list(self.data.movies.columns)
        self.features.remove(self.target[0])
        # standardize data
        self.PredictorScaler = StandardScaler()
        self.TargetVarScaler = StandardScaler()
        self.X, self.y, self.user_row, self.PredictorScalerFit, self.TargetVarScalerFit, self.X_train, self.X_test, self.y_train, self.y_test = self.scaling()

    def extract_new_row(self, X, y):
        new_X = X[-1] #wyslac tego xa do ann  
        X_with_deletion = X[:-1]
        y_with_deletion = y[:-1]
        return X_with_deletion, y_with_deletion, new_X

    def scaling(self, with_extraction=False):
        # set predictors' (X) and tagret (y) values
        X = self.data.movies[self.features]
        y = self.data.movies[self.target] 
        new_X = None
    
        # create fit object
        PredictorScalerFit = self.PredictorScaler.fit(X)
        TargetVarScalerFit = self.TargetVarScaler.fit(y)
        # generate standardized values of features and target
        X = PredictorScalerFit.transform(X)
        y = TargetVarScalerFit.transform(y)
        if with_extraction:
            X, y, new_X = self.extract_new_row(X, y)
        else:
            pass

        # split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
        return X, y, new_X, PredictorScalerFit, TargetVarScalerFit, X_train, X_test, y_train, y_test
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # print(self.X_train.shape)
        # print(self.y_train.shape)
        # print(self.X_test.shape)
        # print(self.y_test.shape)




