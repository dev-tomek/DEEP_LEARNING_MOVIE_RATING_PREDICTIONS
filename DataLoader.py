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
       self.byHandRemoval(self.f_movies)
       self.extractor(self.f_movies, 'genres', 'name') #extracting genres
       self.extractor(self.f_movies, 'production_countries', 'iso_3166_1') #extracting country codes
       #self.extractor(self.f_movies, 'production_companies', 'name') #extracting country codes

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
        final_list = []
        for genre in f_movies['genres']:
            if genre == '[]':
                final_genres.append([])
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
            final_list.append(final_genres)
        f_movies['genres'] = final_list

    def byHandRemoval(self, f_movies):
        """
        removes certain unpleasant values by hand
        """
        f_movies.loc[f_movies.title == "Adanggaman", "production_countries"] = """[{'iso_3166_1': 'CI', 'name': "Cote D_Ivoire"}, {'iso_3166_1': 'BF', 'name': 'Burkina Faso'}, {'iso_3166_1': 'FR', 'name': 'France'}, {'iso_3166_1': 'IT', 'name': 'Italy'}, {'iso_3166_1': 'CH', 'name': 'Switzerland'}]"""
        f_movies.loc[f_movies.title == "Black and White in Color", "production_countries"] = """[{'iso_3166_1': 'CI', 'name': "Cote D_Ivoire"}, {'iso_3166_1': 'FR', 'name': 'France'}, {'iso_3166_1': 'DE', 'name': 'Germany'}, {'iso_3166_1': 'CH', 'name': 'Switzerland'}]"""
        f_movies.loc[f_movies.title == "The Rocket", "production_countries"] = """[{'iso_3166_1': 'AU', 'name': 'Australia'}, {'iso_3166_1': 'LA', 'name': "Lao People_s Democratic Republic"}, {'iso_3166_1': 'TH', 'name': 'Thailand'}]"""
        f_movies.loc[f_movies.title == "Chanthaly", "production_countries"] = """[{'iso_3166_1': 'LA', 'name': "Lao People_s Democratic Republic"}]"""
        f_movies.loc[f_movies.title == "River", "production_countries"] = """[{'iso_3166_1': 'CA', 'name': 'Canada'}, {'iso_3166_1': 'LA', 'name': "Lao People_s Democratic Republic"}]"""

    def extractor(self, f_movies, column, dict_key):
        """
        converts from string to dictionary and extracts values from particulary key
        """
        final_list = []
        for row in f_movies[column]:
            if row == '[]':
                final_list.append(['unknown_'+column])
            else:
                final_values = []    
                row = row.strip('[]').replace("'", "\"")
                for i in range(len(row)):
                    if row[i] == ',':
                        if row[i-1] != '}':
                            pass
                        else:
                            row = row[:i] + '@' + row[i + 1:]
                row = row.replace(" ", "").split('@')
                for item in row: #for each dictionary in a row
                    tmp = json.loads(item) #load that dict
                    final_values.append(tmp[dict_key]) #extract value
                final_list.append(final_values)
        f_movies[column] = final_list