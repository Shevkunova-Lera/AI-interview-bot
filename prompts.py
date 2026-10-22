def get_concept_prompt(concept: str) -> str:
    return f"Please explain '{concept}' in the context of software engineering and machine learning. Keep it precise."

def get_practice_prompt(topic: str, difficulty: str) -> str:
    return f"Generate a {difficulty}-level technical interview question focused on '{topic}'. Do not provide the answer."

def get_feedback_prompt(user_answer: str) -> str:
    return f"Evaluate the following answer or code snippet:\n{user_answer}\nProvide professional, constructive feedback as an interviewer."