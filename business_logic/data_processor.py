import csv
import os


from model.movie_rate import MovieRate
from model.user import User
from model.movie_with_name import  Movie_With_Name

# This is just a processor for csv files. It can create a list of users
class DataProcessor:
    __rates_path: str
    __context_place_path: str
    __context_day_path: str
    __movie_names_path: str

    __movies_from_file: []

    def __init__(self,
                 rates_path: str,
                 context_place_path: str,
                 context_day_path: str,
                 movie_names_path: str):
        assert os.path.exists(rates_path) and os.path.splitext(rates_path)[-1].lower() == '.csv', \
            'Incorrect data file.'
        assert os.path.exists(context_place_path) and os.path.splitext(context_place_path)[-1].lower() == '.csv', \
            'Incorrect context_place file.'
        assert os.path.exists(context_day_path) and os.path.splitext(context_day_path)[-1].lower() == '.csv', \
            'Incorrect context_day file.'
        assert os.path.exists(movie_names_path) and os.path.splitext(context_day_path)[-1].lower() == '.csv', \
            'Incorrect movie_names file.'
        self.__rates_path = rates_path
        self.__context_place_path = context_day_path
        self.__context_day_path = context_day_path
        self.__movie_names_path = movie_names_path
        self.__movies_from_file = []


    def get_real_movie_name(self, basic_movie_name: str):
        if (self.__movies_from_file.__len__() == 0):
            self.__movies_from_file = self.get_movie_list_from_file()
        result = next(filter(lambda m: m.basic_name == basic_movie_name, self.__movies_from_file)).real_name;
        return result;

    def get_movie_list_from_file(self):
        movies = []
        with open(self.__movie_names_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_reader.fieldnames = "basic_name", "real_name"
            for row in csv_reader:
                new_movie = Movie_With_Name()
                new_movie.basic_name = row["basic_name"]
                new_movie.real_name = row["real_name"]
                movies.append(new_movie);
        return movies

    def get_users(self, mode):
        if mode == 'full':
            users_with_rates = self.__create_users_from_data('rate')
            users_with_day_context = self.__create_users_from_data('day')
            users_with_place_context = self.__create_users_from_data('place')
            return self.__merge_users_info(users_with_rates, users_with_day_context, users_with_place_context)
        else:
            return self.__create_users_from_data('rate')

    @staticmethod
    def __merge_users_info(users_with_rates, users_with_day_context, users_with_place_context):
        i = 0
        for user in users_with_rates:
            user_with_day = users_with_day_context[i]
            user_with_place = users_with_place_context[i]
            i += 1
            j = 0
            for movie in user.movies:
                movie_with_day = user_with_day.movies[j]
                movie_with_place = user_with_place.movies[j]
                movie.context_day = movie_with_day.context_day
                movie.context_place = movie_with_place.context_place
                j += 1
        return users_with_rates

    def __create_users_from_data(self, type):
        if type == 'rate':
            path = self.__rates_path
        elif type == 'day':
            path = self.__context_day_path
        elif type == 'place':
            path = self.__context_place_path
        users = []
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user = self.__create_user_from_data_row(row, type)
                users.append(user)
            return users

    @staticmethod
    def __create_user_from_data_row(row, type):
        user = User()
        for key, value in row.items():
            if key == '':
                user.name = value.lstrip().rstrip()
                user.movies = []
            else:
                new_movie = MovieRate()
                new_movie.name = key.lstrip().rstrip()
                if type == 'rate':
                    new_movie.rate = int(value)
                    new_movie.rate_was_given = new_movie.rate != -1;
                elif type == 'day':
                    new_movie.context_day = value.lstrip().rstrip()
                elif type == 'place':
                    new_movie.context_place = value.lstrip().rstrip()

                user.movies.append(new_movie)
        return user
