import pathlib
from backend.directory.getinput import GetInputs

class Test:
    def __init__(self, assignment, directory):
        self.assignment = assignment
        self.dir = pathlib.Path(directory, assignment)

    def check(self):
        """For all questions in assignment, log all test cases that are passed ver total test cases"""
        questions = GetInputs(self.dir, solution=False)
        passed = 0
        total = 0
        for question in questions.questions:
            pass

        return total/passed
        ...

        
