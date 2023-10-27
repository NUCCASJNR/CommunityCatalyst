import requests
from os import getenv
import secrets
paystack_key = getenv('PAYSTACK_KEY')

def initialize_transaction(amount, project_id, user_id):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {paystack_key}",
        "Content-Type": "application/json"
    }
    
    # Generate a unique reference by including user and project information
    reference = f'project_{project_id}_user_{user_id}_payment'
    
    data = {
        'amount': amount * 100,
        'email': 'user_email@gmail.com',  # Use the user's email
        'reference': reference,
        'currency': 'NGN',
        'callback_url': 'https://your-callback-url.com',
        'metadata': {
            'project_id': project_id,
            'user_id': user_id,
        }
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Successful response
        result = response.json()
        # return result['data']['authorization_url']
        return result
    
    else:
        # Handle the error or return an error message
        return f"Error: {response.status_code} - {response.text}"

# Call the function with user-specific data
user_id = secrets.token_hex(6)
response_data = initialize_transaction(100, 100, user_id)
print(response_data)
