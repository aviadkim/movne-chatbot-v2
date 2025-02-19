from huggingface_hub import HfApi
import os

def test_token():
    token = os.getenv('HUGGINGFACE_TOKEN')
    if not token:
        print('Error: HUGGING_FACE_TOKEN not found in environment variables')
        return False
    api = HfApi()
    try:
        user = api.whoami(token=token)
        print(f'Successfully authenticated as: {user}')
        return True
    except Exception as e:
        print(f'Authentication failed: {e}')
        return False

if __name__ == '__main__':
    test_token()