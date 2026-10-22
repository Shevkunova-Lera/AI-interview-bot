import time
from google import genai

class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "parts": [{"text": content}]})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> list:
        return self.history

    def clear(self):
        self.history = []

def stream_interview_response(client: genai.Client, model_name: str, messages: list, retries: int = 3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content_stream(
                model=model_name,
                contents=messages
            )
            print("\nInterviewer: ", end="", flush=True)
            
            full_response = ""
            for chunk in response:
                text = chunk.text
                print(text, end="", flush=True)
                full_response += text
                
            print("\n")
            return full_response
            
        except Exception as e:
            # Exponential backoff: 2^0=1s, 2^1=2s, 2^2=4s
            wait_time = 2 ** attempt
            print(f"\n[API Error. Attempt {attempt + 1}/{retries}]: {e}")
            print(f"Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            
    print("\n[Failure] Could not get a response from the server. Please try again later.")
    return None