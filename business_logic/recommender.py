from copy import deepcopy

from business_logic.rates_calculator import RatesCalculator
from business_logic.similarity_calculator import SimilarityCalculator


class Recommender():
    users: []
    similarity_calculator: SimilarityCalculator
    rates_calculator: RatesCalculator

    def __init__(self, users):
        self.similarity_calculator = SimilarityCalculator(users)
        self.users = users
        self.rates_calculator = RatesCalculator(users)

    # The idea is to get rates for movies similar to the first task way. But only take into an account those movies,
    # which have similar context, i. e. have been watched in the same place/places and in the same days.
    # We also will not recommend movie, which has rate prediction lesser than 4.
    def reccommend_movie(self, user, context):
        if not hasattr(user, 'similar_users') or len(user.similar_users) == 0:
            user.similar_users = self.similarity_calculator.get_similar_users(user)
        self.rates_calculator.get_missing_rates_for_user(user)

        movies_for_context = []
        for movie in user.movies:
            if not movie.rate_was_given:
                movie_for_context = deepcopy(movie)
                movie_for_context.rate = self.rates_calculator.get_rate_for_movie_with_context(user, movie, context)
                if (movie_for_context.rate != -1):
                    movies_for_context.append(movie_for_context)
        movies_for_context.sort(key=lambda x: x.rate, reverse=True)
        result = movies_for_context[0]
        if result.rate >= 4:
            return result
        else:
            return -1



