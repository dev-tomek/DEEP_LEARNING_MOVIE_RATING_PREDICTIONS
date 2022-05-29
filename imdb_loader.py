from modules import *

imdb_columns = {1 : 'Poster_Link',
                2 : 'Series_Title',
                3 : 'Released_Year', 
                4 : 'Certificate',
                5 : 'Runtime', 
                6 : 'Genre', 
                7 : 'IMDB_Rating', 
                8 : 'Overview', 
                9 : 'Meta_score', 
                10 :'Director', 
                11 : 'Star1', 
                12 : 'Star2', 
                13 : 'Star3', 
                14 : 'Star4', 
                15 : 'No_of_Votes', 
                16 : 'Gross'}






class ImbdData:
    def __init__(self):
        self.include_columns = [imdb_columns[3],
                                imdb_columns[4],
                                imdb_columns[5],
                                imdb_columns[6],
                                imdb_columns[7],
                                imdb_columns[9],
                                imdb_columns[15],
                                imdb_columns[16]]
        self.imdb = pd.read_csv('Datafiles\\imdb_top_1000.csv', sep = ',', \
                                    low_memory=False, usecols=self.include_columns)

imdb = ImbdData()
print(imdb.imdb)

        