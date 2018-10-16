from model.user import User
import math

# It should probably be two separated things for similarity and rates calculation.
# I was going to create something good looking and kinda oop, but something went wrong.
# So here it is.
class SimilarityCalculator:
    users: []

    def __init__(self, users):
        self.users = users
        self.get_average_rates_for_users(self.users)

    # This method is used to get average rates for all users. It's been called in constructor, because
    # average rates are needed for calculations anyway. But it can be used on its own for some purposes.
    @staticmethod
    def get_average_rates_for_users(users: []):
        for user in users:
            average_rate = 0
            rates_count = 0
            for movie in user.movies:
                if movie.rate != -1:
                    average_rate += movie.rate
                    rates_count += 1
            average_rate = round(average_rate / rates_count, 3)
            user.average_rate = average_rate

    # This looks kinda terrible, but it is actually a method to find similar users to a given one, using that formula
    # for the task. I hope, it works right. It should.
    def get_similar_users(self, given_user: User, max_amount=7):
        similar_users = []
        for other_user in self.users:
            if other_user.name != given_user.name:
                similarity_numerator = 0
                denominator_gu = 0
                denominator_ou = 0
                i = 0
                for other_user_movie in other_user.movies:
                    given_user_movie = given_user.movies[i]
                    ou_rate = other_user_movie.rate
                    gu_rate = given_user_movie.rate
                    if ou_rate != -1 and gu_rate != -1:
                        similarity_numerator += ou_rate * gu_rate
                        denominator_ou += ou_rate * ou_rate
                        denominator_gu += gu_rate * gu_rate
                    i += 1
                if denominator_ou != 0 and denominator_gu != 0:
                    denominator_ou = round(math.sqrt(denominator_ou),3)
                    denominator_gu = round(math.sqrt(denominator_gu),3)
                similarity_denominator = round(denominator_gu * denominator_ou, 3)
                similarity = round(similarity_numerator / similarity_denominator, 3)
                similar_users.append({'user':other_user, 'similarity': similarity})
        similar_users.sort(key=lambda x: x['similarity'], reverse=True)
        similar_users = similar_users[:max_amount]
        return similar_users



