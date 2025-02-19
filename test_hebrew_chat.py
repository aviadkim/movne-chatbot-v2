import requests
import json

def test_hebrew_chat():
    # Test cases in Hebrew
    test_cases = [
        {
            "message": "שלום, אני מתעניין במוצרים מובנים. האם תוכל להסביר לי מה זה?",
            "description": "Basic question about structured products"
        },
        {
            "message": "מה היתרונות של השקעה במוצרים מובנים?",
            "description": "Benefits of structured products"
        },
        {
            "message": "האם יש הגנת הון במוצרים שלכם?",
            "description": "Question about capital protection"
        }
    ]

    url = 'http://localhost:8000/api/v1/chat'
    headers = {'Content-Type': 'application/json'}

    for test_case in test_cases:
        print(f"\nTesting: {test_case['description']}")
        print(f"Query: {test_case['message']}")
        
        try:
            response = requests.post(
                url,
                json={
                    'message': test_case['message'],
                    'language': 'he',
                    'is_qualified': False
                },
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result['response']}\n")
            else:
                print(f"Error: Status code {response.status_code}")
                print(f"Response: {response.text}\n")
                
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == '__main__':
    test_hebrew_chat()