import requests
import json

def test_bilingual_chat():
    base_url = 'http://localhost:8000/api/v1/chat'
    
    # Test English
    english_response = requests.post(
        base_url,
        json={'message': 'Hello, how are you?', 'language': 'en'}
    )
    print('\nEnglish Test:')
    print('Request: "Hello, how are you?"')
    print('Response:', json.dumps(english_response.json(), indent=2))
    
    # Test Hebrew
    hebrew_response = requests.post(
        base_url,
        json={'message': 'שלום, מה שלומך?', 'language': 'he'}
    )
    print('\nHebrew Test:')
    print('Request: "שלום, מה שלומך?"')
    print('Response:', json.dumps(hebrew_response.json(), indent=2))

if __name__ == '__main__':
    try:
        test_bilingual_chat()
    except requests.exceptions.ConnectionError:
        print('Error: Could not connect to the server. Make sure the server is running on http://localhost:8000')
    except Exception as e:
        print(f'Error: {str(e)}')