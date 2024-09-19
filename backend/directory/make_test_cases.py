import pathlib


class Make_Files:
    def make_question_description(description, directory, file_name):
        """
        Makes txt files with given 'file_name' and description' messages and store it in 'directory'
        """
        destination = pathlib.Path(directory, f'{file_name}.txt')
        with open(destination) as file:
            file.writelines(description)
    
    def make_test_files(description, directory):
        pass