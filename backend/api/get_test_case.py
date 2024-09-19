from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

class ASK_GPT4:
    def __init__(self, secret_key, endpoint, model_name):
        self.model = model_name
        self.client = ChatCompletionsClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(secret_key),
                )

    
    def get_test_cases(self, question, subject):
        response = self.client.complete(
            model=self.model,
            messages=[
                SystemMessage(content=f"You are an experienced {subject} tester."),
                UserMessage(content=f"""Question:{question}
                            Give Me few but enough Test Cases for testing the logic and rebustness of a solution to the given question in a way that I can just copy paste into a {subject} file and run my tests. The format of your response should be:
                            Question: `question`
                            Test Case 1:
                            if solution(parameter1, parameter2) == expected_answer:
                                return True
                            else:
                                return False
                            Test Case 2:
                            if solution(test_case_input) == expected_answer:
                                return True
                            else:
                                return False
                            
                            Also give me some Contrains that should apply to the solution made so that I can run the test cases you provided correctly like:
                            - The Function should be named 'solution'
                            - The Function should take 'these parameters' as input.
                            - The Function should ouput in such a way

                            DON'T GIVE ANYTHING ELSE"""),
            ],
            temperature=1.0,
            max_tokens=1000,
            top_p=1.0
            )
        
        return response.choices[0].message.content
    
if __name__ == '__main__':
    import json 
    with open("Keys/tester_config.json") as file:
        config = json.load(file)
        endpoint = config["endpoint"]
        model_name = config["model_name"]
    with open('Keys/key.txt') as file:
        key = file.readline().strip()
    tester = ASK_GPT4(key, endpoint, model_name)
    question = "Given a matrix, write a python function to return the transpose of the matrix."
    subject = "Python"
    tests = tester.get_test_cases(question, subject)
    print(tests)
    