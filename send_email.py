import requests
from os import getenv
api_key = getenv("ELASTIC_EMAIL")
url = "https://api.elasticemail.com/v2/email/send"

payload = {
    "apikey": api_key,
    "from": "info@community-catalyst.codewithalareef.tech",
    "to": "alareefadegbite@gmail.com",
    "subject": "Test Email",
    "body": "This is a test email.",
}


response = requests.post(url, data=payload)

if response.status_code == 200:
    print("Email sent successfully.")
else:
    print("Failed to send email.")