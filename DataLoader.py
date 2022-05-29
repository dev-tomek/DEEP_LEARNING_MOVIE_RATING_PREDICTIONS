from modules import *
OTHER_THRESHOLD = 100

class Data:
    def __init__(self):
       self.include_columns = [0, 1, 2, 3, 7, 10, 12, 13, 14, 15, 16, 18, 20, 21, 22, 23] 
       self.movies_org = pd.read_csv('Datafiles\\movies_metadata.csv', sep = ',', \
                                  low_memory=False, usecols=self.include_columns)
       self.f_conditions = (self.movies_org['adult'] == 'False') & \
                         (self.movies_org['status'] == 'Released') & \
                         (self.movies_org['video'] == False)
       self.movies = self.movies_org[self.f_conditions].drop(['adult', 'status', 'video'], axis=1)
        

       self.movies = self.movies.drop(['production_companies'], axis=1)
       self.btc_transform(self.movies)
       self.datatype_conversion(self.movies)
       self.original_language_transform(self.movies)
       self.release_date_transform(self.movies)
       self.data_filter()
       self.byHandRemoval(self.movies)
       self.extractor(self.movies, 'genres', 'name') #extracting genres
       self.extractor(self.movies, 'production_countries', 'iso_3166_1') #extracting country codes
       #self.extractor(self.movies, 'production_companies', 'name') #extracting country codes
       self.one_hot_encode(self.movies, 'genres')
       self.one_hot_encode(self.movies, 'original_language')
       self.movies = self.movies.rename(columns=str.lower)
       self.production_country_transform(self.movies)
       self.one_hot_encode(self.movies, 'production_countries')

       self.movies = self.movies[(self.movies['vote_count'] > 1)
       & (self.movies['budget'] > 10) 
       & (self.movies['popularity'] > 10)
       & (self.movies['runtime'] > 10)
       & (self.movies['revenue'] > 10)]
       

    def btc_transform(self, movies):
        """
        btc_transform stands for 'belongs_to_collection' column transformation
        if value is missing it replaces it with 0 and otherwise with 1
        """
        movies.loc[movies['belongs_to_collection'].notna(), 'belongs_to_collection'] = 1
        movies.loc[movies['belongs_to_collection'].isna(), 'belongs_to_collection'] = 0
        

    def datatype_conversion(self, movies):                                                                        ##################
        """
        converts datatypes of chosen columns
        """
        movies['budget'] = movies['budget'].astype(int)
        movies['popularity'] = movies['popularity'].astype(float)
        movies['release_date'] = movies['release_date'].astype(str)
        movies['original_language'] = movies['original_language'].astype(str)
        movies['belongs_to_collection'] = movies['belongs_to_collection'].astype(int)

    def original_language_transform(self, movies):
        """
        - changes the 'original_language' column type to string
        - counts the number of instances of each language
        - groups languages with small number of occurances (below the threshold amount) into one group
        called 'other'
        """
        
        lang = movies['original_language'].value_counts()
        lang_other = lang[lang <= OTHER_THRESHOLD]
        movies.loc[movies['original_language'].isin(lang_other.index.to_list()), 'original_language'] = 'other_language'

    def release_date_transform(self, movies):
        """
        extracts the year from the release date, and sets the nones to 0
        """
        movies.loc[movies['release_date'] == 'nan', 'release_date'] = '0000'
        movies['release_date'] = movies['release_date'].str[:4]
        movies['release_date'] = pd.to_numeric(movies['release_date'])

    def data_filter(self):
        """
        gets rid of particular data
        """
        self.movies = self.movies[self.movies['vote_count'] != 0]
        self.movies = self.movies[self.movies['release_date'] != 0]

    def byHandRemoval(self, movies):
        """
        removes certain unpleasant values by hand and drops title column
        """
        movies.loc[movies.title == "Adanggaman", "production_countries"] = """[{'iso_3166_1': 'CI', 'name': "Cote D_Ivoire"}, {'iso_3166_1': 'BF', 'name': 'Burkina Faso'}, {'iso_3166_1': 'FR', 'name': 'France'}, {'iso_3166_1': 'IT', 'name': 'Italy'}, {'iso_3166_1': 'CH', 'name': 'Switzerland'}]"""
        movies.loc[movies.title == "Black and White in Color", "production_countries"] = """[{'iso_3166_1': 'CI', 'name': "Cote D_Ivoire"}, {'iso_3166_1': 'FR', 'name': 'France'}, {'iso_3166_1': 'DE', 'name': 'Germany'}, {'iso_3166_1': 'CH', 'name': 'Switzerland'}]"""
        movies.loc[movies.title == "The Rocket", "production_countries"] = """[{'iso_3166_1': 'AU', 'name': 'Australia'}, {'iso_3166_1': 'LA', 'name': "Lao People_s Democratic Republic"}, {'iso_3166_1': 'TH', 'name': 'Thailand'}]"""
        movies.loc[movies.title == "Chanthaly", "production_countries"] = """[{'iso_3166_1': 'LA', 'name': "Lao People_s Democratic Republic"}]"""
        movies.loc[movies.title == "River", "production_countries"] = """[{'iso_3166_1': 'CA', 'name': 'Canada'}, {'iso_3166_1': 'LA', 'name': "Lao People_s Democratic Republic"}]"""
        self.movies = self.movies.drop(['title'], axis=1)

    def extractor(self, movies, column, dict_key):
        """
        converts from string to dictionary and extracts values from particulary key
        """
        final_list = []
        for row in movies[column]:
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
        movies[column] = final_list
    
    def one_hot_encode(self, movies, column_name):
        """
        - takes the column and splits it into multiple one hot encoded ones
        - performs a join on to the data frame
        """
        s = movies[column_name].explode()
        self.movies = movies.drop(column_name, axis = 1).join(pd.crosstab(s.index, s))

    def production_country_transform(self, movies):
        """
        - extracts the first index from the production country list
        - selects the production countries with count higher than a 100
        """
        movies.loc[:, 'production_countries'] = movies['production_countries'].apply(lambda x: x[0])
        countries = movies['production_countries'].value_counts()
        country_other = countries[countries <= OTHER_THRESHOLD]
        movies.loc[movies['production_countries'].isin(country_other.index.to_list()), 'production_countries'] = 'other_country'