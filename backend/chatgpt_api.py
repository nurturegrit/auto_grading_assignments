from openai import OpenAI

class HomeworkGrader:
    def __init__(self, token, endpoint, model_name, assignment,output_limit):
        self.client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )
        self.model_name = model_name
        self.assignment = assignment
        self.output_words = output_limit

    def grade_answer(self, answer):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a master at python algorithms and data structures.",
                },
                {
                    "role": "user",
                    "content": f"Here is My Homework for assignment {self.assignment}. Answer: {answer}. Please Grade it from 1 to 100 and provide short but valuable feedback while telling when and where marks are deducted in a section called Feedback.",
                }
            ],
            model=self.model_name,
            temperature=1.,
            max_tokens=self.output_words,
            top_p=1.
        )
        return response.choices[0].message.content

# Example usage:
# grader = HomeworkGrader(token, endpoint, model_name, assignment)
# feedback = grader.grade_answer(answer)
# print(feedback)

if __name__ == '__main__':
    with open('Keys/key.txt') as file:
        token = file.readline().strip()
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o-mini"
    assignment = 'You are given a list of number. Make a function for finding unique elements'
    grader = HomeworkGrader(token, endpoint, model_name, assignment, 200)
    grade = grader.grade_answer(answer= 'def unique(arr):\nreturn set(arr)')
    print(grade)