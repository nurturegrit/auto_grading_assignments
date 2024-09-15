import os

class GetInputs:
    def __init__(self, dir):
        '''
        dir = assignment_directory with a subdirectory questions, internid, internid2, intern3.. 
        -----------------------------------------------------------------------------------------
        self.questions
        - Initializes questions dictionary that stores questions from text files in questions subdirectory
        self.solutions
        - Initializes a dict to store intern and solutions
        - append format :- {intern_id: {solution_id: 'answer_in_string'} }
        '''
        self.dir = dir
        if not os.path.exists(dir):
            print(f"Directory {dir} does not exist.")
            return
        self.questions = dict()
        self.get_questions()
        self.solutions = dict()
        self.populate_dict()

    
    def get_questions(self):
        dir = os.path.join(self.dir, 'Questions')
        ...

    def populate_dict(self):
        ...