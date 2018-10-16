from business_logic.data_processor import DataProcessor
from business_logic.rates_calculator import RatesCalculator
import business_logic.result_creator as rc

# There are some variables for testing. A program should probably workfor other users too.
data_path = 'sources/data.csv'
context_day_path = 'sources/context_day.csv'
context_place_path = 'sources/context_place.csv'
result_path='result/result.json'
user_name = 'User 6'


def main():
    print('Working on the first task...')
    print('Trying to calculate missing rates for the user: ' + user_name)
    data_processor = DataProcessor(rates_path=data_path,
                                   context_day_path=context_day_path,
                                   context_place_path=context_place_path);
    users = data_processor.get_users('full')
    rates_calculator = RatesCalculator(users)
    current_user = next(filter(lambda u: u.name == user_name, users))
    task_1_result = rates_calculator.get_missing_rates_for_user(current_user)
    rc.create_json(result_path, user_name, task_1_result)
    print('First task seems to be done.')




if __name__ == "__main__":
    main()