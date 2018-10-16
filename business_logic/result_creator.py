def create_json(output_path, user_name, task_1_result):
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
        file.write('"status": ' + '"Not finished yet. Sorry."')
        file.write("}\n")
        file.write("}")
