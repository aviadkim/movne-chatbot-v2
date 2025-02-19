import requests
import json

def test_chat_endpoint():
    base_url = 'http://localhost:8000/api/v1/chat'
    
    # Test cases with different types of questions
    test_cases = [
        {
            'message': 'What investment products do you offer?',
            'language': 'en',
            'is_qualified': False
        },
        {
            'message': 'מהם מוצרי ההשקעה שאתם מציעים?',
            'language': 'he',
            'is_qualified': False
        },
        {
            'message': 'Can you explain the risks involved in structured products?',
            'language': 'en',
            'is_qualified': True
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"\nTesting with message: {test_case['message']}")
            response = requests.post(base_url, json=test_case)
            
            if response.ok:
                print(f"Status Code: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == '__main__':
    test_chat_endpoint()