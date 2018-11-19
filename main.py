from business_logic.data_processor import DataProcessor
from business_logic.rates_calculator import RatesCalculator
from business_logic.wikidata_querier import Wikidata_Querier
import business_logic.result_creator as rc


# There are some variables for testing. A program should probably workfor other users too.
from business_logic.recommender import Recommender

data_path = 'sources/data.csv'
context_day_path = 'sources/context_day.csv'
context_place_path = 'sources/context_place.csv'
movie_names_path = 'sources/Movie_names.csv'
result_path='result/result.json'
query_result_path='result/query_result.json'
query_full_result_path='result/full_query_result.json'
user_name = 'User 6'
context = ({'places':['h']},{'days':['Sat', 'Sun']})    # Haven't checked if it works with another context.
                                                        # But it probably should.


def main():
    print('Working on the first task...')
    print('Trying to calculate missing rates for the user: ' + user_name)
    data_processor = DataProcessor(rates_path=data_path,
                                   context_day_path=context_day_path,
                                   context_place_path=context_place_path,
                                   movie_names_path=movie_names_path);
    users = data_processor.get_users('full')
    rates_calculator = RatesCalculator(users)
    current_user = next(filter(lambda u: u.name == user_name, users))
    task_1_result = rates_calculator.get_missing_rates_for_user(current_user)
    print('First task seems to be done.')
    print('')

    print('Working on the second task...')

    recommender = Recommender(users);
    task_2_result = recommender.reccommend_movie(current_user, context);
    print('Trying to create a recommendation for the user: ' + user_name)
    rc.create_json(result_path, user_name, task_1_result, task_2_result)
    print('Second task seems to be done.')

    print('')


    print('Working on the third task...')
    basic_movie_name = task_2_result.name
    print('Trying to get information about movie: ' + basic_movie_name)
    real_movie_name = data_processor.get_real_movie_name(basic_movie_name)

    wikidata_querier = Wikidata_Querier()

    #for convinience there is a simplified query result which goes to query_result.json
    information = wikidata_querier.get_information_for_movie(real_movie_name = real_movie_name,
                                                             simplify_result = True)
    rc.create_json_for_information(query_result_path, information)

    #there is also a full non simplified result of the query which goes to full_query_result.json
    information = wikidata_querier.get_information_for_movie(real_movie_name=real_movie_name,
                                                             simplify_result=False)
    rc.create_json_for_information(query_full_result_path, information)
    print('Done!')

if __name__ == "__main__":
    main()