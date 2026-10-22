import os
import sys
from dotenv import load_dotenv
from google import genai

# Import our modules
from chatbot import ConversationManager, stream_interview_response
from prompts import get_practice_prompt

def main():
    # 1. Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL ERROR: GEMINI_API_KEY not found in .env file")
        sys.exit(1)

    # Initialization
    client = genai.Client()
    model_name = 'gemini-1.5-flash'
    manager = ConversationManager()

    print("=======================================")
    print("     AI Technical Interview Trainer    ")
    print("=======================================")
    print("Available commands: /help, /practice, /summary, /clear, /quit")

    # 3. CLI interaction loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except KeyboardInterrupt: # Handle Ctrl+C
            print("\nForce quit. Goodbye!")
            break

        # Handle empty input
        if not user_input:
            continue

        command = user_input.lower()

        if command == '/quit':
            print("Exiting the trainer. Good luck on your interviews!")
            break
            
        elif command == '/help':
            print("Commands:")
            print("  /practice - Start a new practice question on a specific topic")
            print("  /summary  - Show session statistics")
            print("  /clear    - Clear conversation history")
            print("  /quit     - Exit the program")
            
        elif command == '/clear':
            manager.clear()
            print("[System]: Conversation history cleared successfully.")
            
        elif command == '/summary':
            # 2. Print message count and approximate token usage
            history = manager.get_history()
            msg_count = len(history)
            # Rough estimation: 1 word ~ 1.3 tokens
            approx_tokens = sum(len(m['parts'][0]['text'].split()) * 1.3 for m in history)
            
            print("--- Session Summary ---")
            print(f"Messages in history: {msg_count} / {manager.max_history}")
            print(f"Approximate context tokens used: ~{int(approx_tokens)}")
            print("-----------------------")
            
        elif command == '/practice':
            topic = input("Enter topic (e.g., Python OOP, SQL, System Design): ").strip()
            difficulty = input("Difficulty level (Junior, Middle, Senior): ").strip()
            
            prompt = get_practice_prompt(topic, difficulty)
            manager.add_message("user", prompt)
            
            response = stream_interview_response(client, model_name, manager.get_history())
            if response:
                manager.add_message("model", response)
                
        else:
            # Regular text response to the interviewer
            manager.add_message("user", user_input)
            response = stream_interview_response(client, model_name, manager.get_history())
            if response:
                manager.add_message("model", response)

if __name__ == "__main__":
    main()