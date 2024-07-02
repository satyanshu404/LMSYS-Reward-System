
def prompt_template(query:str, response_a:str, response_b:str, correct_label:str)->str:
    return f'''
Act like a discriminator assistant which have the capabilities to distinguish between two responses for the given query.
You will be given one query and two responses  and the label to that query. You have to compare the two responses based on the given correct label and provide feedback like
which response is more relevant, accurate, clear, comprehensive, concise, logically flowing, evidence-based, consistent, objective, and responsive to the nuances of the query and why.
If the response A is best then you have to write A, if response B is best then you have to write B and if both are best then you have to write AB.
The feedback should be detailed and provide clear reasoning for each aspect and in reason compare why one response is better and other in bad.
However do not soley rely on the given label and also consider the responses in general.
Output must be in the following JSON format:
Output: {{
    'relevance': {{
        'response': '<A/B/AB> Which response is more relevant to the query?',
        'reason': 'Provide a detailed explanation of why one response directly addresses the query better and provides more pertinent information.'
    }},
    'accuracy': {{
        'response': '<A/B/AB> Which response is more accurate?',
        'reason': 'Explain why one response contains more reliable information based on facts and credible sources.'
    }},
    'clarity': {{
        'response': '<A/B/AB> Which response is clearer?',
        'reason': 'Describe why one response is more straightforward, easy to understand, and free of ambiguity.'
    }},
    'completeness': {{
        'response': '<A/B/AB> Which response is more comprehensive?',
        'reason': 'Detail why one response covers all aspects of the query more thoroughly.'
    }},
    'conciseness': {{
        'response': '<A/B/AB> Which response is more concise?',
        'reason': 'Explain why one response is more succinct and to the point without unnecessary information.'
    }},
    'logical_flow': {{
        'response': '<A/B/AB> Which response has a better logical flow?',
        'reason': 'Discuss why one response presents information in a more organized and coherent manner.'
    }},
    'evidence_examples': {{
        'response': '<A/B/AB> Which response provides stronger evidence and examples?',
        'reason': 'Specify why one response includes stronger or more relevant evidence and examples to support its points.'
    }},
    'consistency': {{
        'response': '<A/B/AB> Which response is more consistent?',
        'reason': 'Clarify why one response maintains internal consistency without contradictions.'
    }},
    'objectivity': {{
        'response': '<A/B/AB> Which response is more objective?',
        'reason': 'Explain why one response is more unbiased and neutral in its presentation.'
    }},
    'responsiveness': {{
        'response': '<A/B/AB> Which response is more responsive to the nuances and sub-questions within the query?',
        'reason': 'Describe why one response better addresses specific details and aspects of the query, including any sub-questions.'
    }}
}}

Task:
Query: {query}
Resonse A: {response_a}
Response B: {response_b}
Correct Label: {correct_label}
Output:
'''