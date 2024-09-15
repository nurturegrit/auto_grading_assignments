from openai import OpenAI

class HomeworkGrader:
    def __init__(self, token, endpoint, model_name, output_limit):
        self.client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )
        self.model_name = model_name
        self.output_words = output_limit

    def grade_answer(self, question, answer, full_score):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a master at python algorithms and data structures. You Always put Score at the front of your feedback like Score: 85/100. If the answer is totally irrelevant to the question or if there is no answer. You are merciless and give 0/100 score.",
                },
                {
                    "role": "user",
                    "content": f"""Here is My Homework for Question {question}.\nAnswer: {answer}.\n\nGrade it from 0 to {full_score}.Provide concise and valuable feedback while telling when marks are deducted.\nProvide Output like 'Score: 85/100\n\nFeedback: Great job! You can improve by optimizing your code further at these points: `bullet points, each one in new line`.\nBest regards,\nSabudh.""",
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
    q = 'You are given a list of number. Make a function for finding unique elements'
    grader = HomeworkGrader(token, endpoint, model_name, 200)
    grade = grader.grade_answer(question=q,answer= 'def unique(arr):\nreturn set(arr)',full_score=100)
    print(grade)