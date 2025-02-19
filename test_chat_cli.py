import requests
import sys
import os

def chat_with_bot(message: str, language: str = "he") -> None:
    # Use Railway URL if available, otherwise fallback to localhost
    api_url = os.getenv('RAILWAY_STATIC_URL', 'http://localhost:8000')
    if not api_url.startswith('http'):
        api_url = f"https://{api_url}"
    
    print(f"\nSending message to {api_url}")
    print(f"Message: {message}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{api_url}/api/chat",
            json={"message": message, "language": language},
            timeout=30  # Increase timeout for model inference
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Bot: {result['response']}\n")
        else:
            print(f"Error: Status code {response.status_code}")
            
    except Exception as e:
        print(f"Error connecting to bot: {str(e)}")

def main():
    print("Movne Chatbot CLI Test")
    print("Type 'exit' to quit")
    print("Type 'lang:en' or 'lang:he' to switch languages")
    
    language = "he"
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                break
                
            if user_input.startswith('lang:'):
                language = user_input.split(':')[1]
                print(f"Language switched to: {language}")
                continue
                
            if user_input:
                chat_with_bot(user_input, language)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
