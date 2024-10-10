from backend.api.get_test_case import ASK_GPT4
from backend.directory.make_test_files import Make_Files
from backend.directory.getinput import GetInputs
import pathlib
import sys

def make_assignment(dir, secret_key, endpoint, model_name):
    test_case_maker = ASK_GPT4(secret_key, endpoint=endpoint, model_name=model_name)
    get_questions = GetInputs(dir=dir, solution=False)
    subject = 'Python'
    for file_name, question in get_questions.questions.items():
        description = test_case_maker.get_test_cases(question, subject)
        Make_Files.make_question(description=description, directory=dir, file_name=file_name)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Input Assignment_Folder as Argument")

    dir = pathlib.Path('Input', sys.argv[1])

    import json
    with open("Keys/tester_config.json") as file:
        config = json.load(file)
        endpoint = config["endpoint"]
        model_name = config["model_name"]

    with open('Keys/key.txt') as file:
        key = file.readline().strip()
        
    make_assignment(dir, key, endpoint, model_name)