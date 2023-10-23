#!/usr/bin/env python3

import requests
from os import getenv

API_KEY = getenv("PAYSTACK_KEY")
# print(API_KEY)
url = "https://api.paystack.co/dedicated_account"
headers = {
    "Authorization": f'BEARER {API_KEY}',
    "Content-Type": "application/json"
}
data = {
    "customer": 'CUS_2n1b2gp5tw5bwwm',
    "preferred_bank": "wema-bank"
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("Request was successful")
    print(response.json())
else:
    print("Request failed with status code:", response.status_code)
    print(response.text)


# url = "https://api.paystack.co/customer/alareefadegbite@gmail.com"
# headers = {
#     "Authorization": f"BEARER {API_KEY}",
#     "Content-Type": "application/json"
# }
# data = {
#     "email": "idan@gmail.com",
#     "first_name": "test",
#     "last_name": "new customer",
#     "phone": "+2348123456789"
# }
#
# response = requests.post(url, headers=headers, json=data)
#
# if response.status_code == 200:
#     print("Request was successful")
#     print(response.json())
# else:
#     print("Request failed with status code:", response.status_code)
#     print(response.text)

# new_req = requests.get(url, headers=headers)
# if new_req.status_code == 200:
#     print('Request Successful')
#     print(new_req.json())
# else:
#     print("Request failed with status code:", new_req.status_code)
#     print(new_req.text)
