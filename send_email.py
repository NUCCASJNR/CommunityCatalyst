#!/usr/bin/env python3
import requests
from os import getenv
api_key = getenv("ELASTIC_EMAIL")
url = "https://api.elasticemail.com/v2/email/send"

payload = {
    "apikey": api_key,
    "from":"community-catalyst@polyglotte.tech",
    "to": "alareefadegbite@gmail.com",
    "subject": "Test Email",
    "body": "This is a test email.",
}


response = requests.post(url, data=payload)

if response.status_code == 200:
    print(response.json())
else:
    print("Failed to send email.")
