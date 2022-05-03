from modules import *
OTHER_THRESHOLD = 100

class Data:
    def __init__(self):
       self.include_columns = [0, 1, 2, 3, 7, 10, 12, 13, 14, 15, 16, 18, 20, 21, 22, 23] 
       self.movies = pd.read_csv('Datafiles\\movies_metadata.csv', sep = ',', \
                                  low_memory=False, usecols=self.include_columns)
       self.f_conditions = (self.movies['adult'] == 'False') & \
                         (self.movies['status'] == 'Released') & \
                         (self.movies['video'] == False)
       self.f_movies = self.movies[self.f_conditions].drop(['adult', 'status', 'video'], axis=1)
       self.btc_transform(self.f_movies)
       self.original_language_transform(self.f_movies)
       self.genre_extractor(self.f_movies)

    def btc_transform(self, f_movies):
        """
        btc_transform stands for 'belongs_to_collection' column transformation
        if value is missing it replaces it with 0 and otherwise with 1
        also changes the column type to int
        """
        f_movies.loc[f_movies['belongs_to_collection'].notna(), 'belongs_to_collection'] = 1
        f_movies.loc[f_movies['belongs_to_collection'].isna(), 'belongs_to_collection'] = 0
        f_movies['belongs_to_collection'] = f_movies['belongs_to_collection'].astype(int)

    def original_language_transform(self, f_movies):
        """
        - changes the 'original_language' column type to string
        - counts the number of instances of each language
        - groups languages with small number of occurances (below the threshold amount) into one group
        called 'other'
        """
        f_movies['original_language'] = f_movies['original_language'].astype(str)
        lang = f_movies['original_language'].value_counts()
        lang_other = lang[lang <= OTHER_THRESHOLD]
        f_movies.loc[f_movies['original_language'].isin(lang_other.index.to_list()), 'original_language'] = 'other'

    def genre_extractor(self, f_movies):
        """
        extracts the genres from the dictionaries contained in the 'genre' column
        """
        for genre in f_movies['genres']:
            if genre == '[]':
                genre = []
            else:
                final_genres = []
                genre = genre.strip('[]').replace("'", "\"")
                for i in range(len(genre)):
                    if genre[i] == ',':
                        if genre[i-1] != '}':
                            pass
                        else:
                            genre = genre[:i] + '@' + genre[i + 1:]
                genre = genre.split('@')
                for item in genre:   
                    tmp = json.loads(item)
                    final_genres.append(tmp['name'])
                genre = final_genres




        # stripped = f_movies['genres'][0].strip('[]')
        # json_adjusted = stripped.replace("'", "\"")
        # for i in range(len(json_adjusted)):
        #     if json_adjusted[i] == ',':
        #         if json_adjusted[i-1] != '}':
        #             pass
        #         else:
        #             json_adjusted = json_adjusted[:i] + '@' + json_adjusted[i + 1:]

        # json_adjusted = json_adjusted.split('@')
        # for item in json_adjusted:
        #     tmp = json.loads(item)
        #     print(type(tmp))
        #     print(tmp)









        #s = df[0]
        #print(df['belongs_to_collection'][0])
        # json_acceptable_string = s.replace("'", "\"")
        # d = json.loads(json_acceptable_string)
        # print(d)
        # print(type(d))
        # print(d['id'])s
