from sqlite3 import DatabaseError
from modules import *


class UserInput:
    def __init__(self):
        self.train_and_test = TrainAndTest.TrainAndTest()
        self.data = DataLoader.Data()
        self.entries = ['0','0','0','0','0','0','0','0','0','0']
        self.new_row = self.create_row()

    def create_row(self):
        new_row = pd.DataFrame(np.zeros((1, len(self.data.movies.columns.tolist()))), columns = self.data.movies.columns)
        new_row.loc[[0], :'vote_count'] = [self.entries[0], #collection
                                                self.entries[1], #budget
                                                self.entries[2], #popularity
                                                self.entries[3], #release_date
                                                self.entries[4], #revenue
                                                self.entries[5], #runtime
                                                0,
                                                self.entries[6] #vote count  
                                                ]                                   

        self.genre = self.entries[7].lower()
        self.original_language = self.entries[8].lower()
        self.production_country = self.entries[9].upper()
        
        if self.genre in new_row.columns.tolist():
            new_row.loc[[0], self.genre] = 1
        else:
            new_row.loc[[0], 'unknown_genres'] = 1

        if self.original_language in new_row.columns.tolist():
            new_row.loc[[0], self.original_language] = 1
        else:
            new_row.loc[[0], 'other_language'] = 1

        if self.production_country in new_row.columns.tolist():
            new_row.loc[[0], self.production_country] = 1
        else:
            new_row.loc[[0], 'other_country'] = 1

        return new_row
    
    def send_row(self):
        self.train_and_test.input_row = self.new_row
        self.train_and_test.data.movies.append(self.new_row)

