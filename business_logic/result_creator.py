import json

# That is probably not the best way to create a .json file. But it is much easier than generation of object having
# necessary format.


def create_json(output_path, user_name, task_1_result, task_2_result):
    with open(output_path, 'w') as file:
        file.write("{\n")
        file.write('"user": ' + user_name[-1] + ",\n")
        file.write('"1":' + " { \n")
        for movie in task_1_result.movies:
            if movie.name != 'Movie 30':
                file.write('"' + movie.name + '": ' + str(movie.rate) + ",\n")
            else:
                file.write('"' + movie.name + '": ' + str(movie.rate) + "\n")
        file.write("},\n")
        file.write('"2":' + " {\n")
        if task_2_result != -1:
            file.write('"' + task_2_result.name +'":'  + str(task_2_result.rate))
        else:
            file.write('"no such movie":' + '-')
        file.write("}\n")
        file.write("}")


def create_json_for_information(output_path, data):
    with open(output_path, 'w') as file:
        json.dump(data, file)
