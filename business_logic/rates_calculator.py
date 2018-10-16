from business_logic.similarity_calculator import SimilarityCalculator
from model.user import User

class RatesCalculator():
    similarity_calculator: SimilarityCalculator
    users: []

    def __init__(self, users):
        self.users = users
        self.similarity_calculator = SimilarityCalculator(users)

    # This method may be used to get rate for a user's movie.
    # If it's already rated, then you get existing rate.
    # If there is not enough similar users (none) to get rate, you shall get -1 again.
    # It could be alternated alongside with get_similar_users method to find top 7 similar users, which have
    # rates for the given movie.
    @staticmethod
    def get_rate_for_movie(user, movie):
        user_movie = next(filter(lambda m: m.name == movie.name, user.movies))
        if user_movie.rate != -1:
            return user_movie.rate
        numerator = 0
        denominator = 0
        for similar_user in user.similar_users:
            su_movie = next(filter(lambda m: m.name == movie.name, similar_user['user'].movies))
            if su_movie.rate != -1:
                numerator += round(similar_user['similarity'] * (su_movie.rate - similar_user['user'].average_rate), 3)
                denominator += similar_user['similarity']

        if denominator != 0:
            rate = user.average_rate + round(numerator / denominator, 3)
            return rate
        else:
            return -1

    # This method can be used to find all missing rates for the user's movies. Well, if at least one of the
    # similar users has already rated the movie.
    def get_missing_rates_for_user(self, user):
        user.similar_users = self.similarity_calculator.get_similar_users(user)
        for movie in user.movies:
            movie.rate = self.get_rate_for_movie(user, movie)
        return user


