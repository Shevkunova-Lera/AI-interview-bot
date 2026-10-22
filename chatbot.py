from google import genai

class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        # Формат 'role' может быть 'user' или 'model'
        self.history.append({"role": role, "parts": [{"text": content}]})
        # Обрезаем старые сообщения, чтобы не превышать лимиты токенов
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> list:
        return self.history

    def clear(self):
        self.history = []

def stream_interview_response(client: genai.Client, model_name: str, messages: list):
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
        print(f"\n[Connection Error]: {e}")
        return None