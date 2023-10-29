import requests
import secrets
from os import getenv

paystack_key = getenv('PAYSTACK_KEY')

def initialize_and_verify_transaction(amount, project_id, user_id):
    # Initialize the transaction
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {paystack_key}",
        "Content-Type": "application/json"
    }
    
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
        result = response.json()
        reference = result['data']['reference']
        
        # Verify the transaction
        verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
        verify_headers = {
            "Authorization": f"Bearer {paystack_key}",
        }
        
        verify_response = requests.get(verify_url, headers=verify_headers)

        if verify_response.status_code == 200:
            return verify_response.json()['data']['status']
        else:
            return f"Error: {verify_response.status_code} - {verify_response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Call the function with user-specific data
user_id = secrets.token_hex(6)
response_data = initialize_and_verify_transaction(100, 100, user_id)
print(response_data)

