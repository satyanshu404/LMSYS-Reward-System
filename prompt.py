
def prompt_template(query:str, response_a:str, response_b:str, correct_label:str)->str:
    return f'''
Act as a discriminator assistant to evaluate and distinguish between two responses for a given query based on the given label.
You will be provided with a query, two responses and the correct label. Your task is to compare the responses based on various criteria and determine which one is superior in each aspect.
However do not soley rely on the given label and also consider the responses in general.

The criteria are:
Relevance: Which response directly addresses the query better and provides more pertinent information?
Accuracy: Which response contains more reliable and factual information based on credible sources?
Clarity: Which response is more straightforward, easy to understand, and free of ambiguity?
Completeness: Which response covers all aspects of the query more thoroughly?
Conciseness: Which response is more succinct and to the point without unnecessary information?
Logical Flow: Which response presents information in a more organized and coherent manner?
Evidence & Examples: Which response provides stronger evidence and examples?
Consistency: Which response maintains internal consistency without contradictions?
Objectivity: Which response is more unbiased and neutral?
Responsiveness: Which response better addresses specific details and aspects of the query?

For each criterion, assign one of the following ratings:
A: Response A is superior
B: Response B is superior
AB: Both responses are equally optimal
NA: Neither response is satisfactory

Provide output as a comma-separated list of ratings, corresponding to the order of criteria listed above.
For example:
Output: A,A,NA,AB,B,B,A,A,AB,B

###IMPORTANT NOTES:
- Do not include any explanations or additional text. Simply provide the comma seperated ratings.
- The order of ratings should match the order of criteria listed above.
- There must be exactly 10 ratings in the output.

###Task:
Query: {query}
Resonse A: {response_a}
Response B: {response_b}
Correct Label: {correct_label}
Output:
'''


def response_generator_prompt(query:str, response_a:str, response_b:str, correct_label:str)->str:
    return f'''
As a discriminator professionalist, I have the capability to distinguish between two responses to a given query. 
My task is to compare the two responses based on the given correct label and provide feedback on various aspects of their quality. 
Here's how I will proceed:
 
###Input
I will receive the following inputs:

Query: The question or problem statement that the responses are addressing.
Response A: The first response to the query.
Response B: The second response to the query.
Correct Label: The label indicating which response is deemed correct or most appropriate.
###Output
I will evaluate and compare the two responses across multiple criteria, and provide a detailed explanation for each criterion. 
The output will be in JSON format with the following structure:
Output:{{
    "response": {{
        "response": "<A/B/AB/NA> Which response is more relevant to the query?",
        "reason": "Provide a detailed explanation of why one response directly addresses the query better and provides more pertinent information."
    }},
    "accuracy": {{
        "response": "<A/B/AB/NA> Which response is more accurate?",
        "reason": "Explain why one response contains more reliable information based on facts and credible sources."
    }},
    "clarity": {{
        "response": "<A/B/AB/NA> Which response is clearer?",
        "reason": "Describe why one response is more straightforward, easy to understand, and free of ambiguity."
    }},
    "completeness": {{
        "response": "<A/B/AB/NA> Which response is more comprehensive?",
        "reason": "Detail why one response covers all aspects of the query more thoroughly."
    }},
    "conciseness": {{
        "response": "<A/B/AB/NA> Which response is more concise?",
        "reason": "Explain why one response is more succinct and to the point without unnecessary information."
    }},
    "logical_flow": {{
        "response": "<A/B/AB/NA> Which response has a better logical flow?",
        "reason": "Discuss why one response presents information in a more organized and coherent manner."
    }},
    "evidence_examples": {{
        "response": "<A/B/AB/NA> Which response provides stronger evidence and examples?",
        "reason": "Specify why one response includes stronger or more relevant evidence and examples to support its points."
    }},
    "consistency": {{
        "response": "<A/B/AB/NA> Which response is more consistent?",
        "reason": "Clarify why one response maintains internal consistency without contradictions."
    }},
    "objectivity": {{
        "response": "<A/B/AB/NA> Which response is more objective?",
        "reason": "Explain why one response is more unbiased and neutral in its presentation."
    }},
    "responsiveness": {{
        "response": "<A/B/AB/NA> Which response is more responsive to the nuances and sub-questions within the query?",
        "reason": "Describe why one response better addresses specific details and aspects of the query, including any sub-questions."
    }}
}}

###Evaluation Process
For each criterion, I will:

- Compare both responses.
- Provide a verdict on which response (A, B, AB, NA) best meets the criterion.
- Offer a detailed explanation for my decision with evidence from the text, comparing the strengths and weaknesses of each response.

###Task:
Query: {query}
Resonse A: {response_a}
Response B: {response_b}
Correct Label: {correct_label}
Output:
'''