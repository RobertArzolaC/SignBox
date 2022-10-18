import os
import requests

from .constants import BASE_API


SERVER_PROJECT = os.getenv("SERVER_PROJECT", "uanataca")


class SignBox:
    api_url = BASE_API

    def __init__(self, username, password, pin):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.pin = pin
        self.build_headers()
        self.build_payload()
        
    def build_headers(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
    def build_payload(self):
        self.payload = {
            'urlback': f'{SERVER_PROJECT}/servicelogs',
            'url_out': f'{SERVER_PROJECT}/result_book1',
            'env': 'test',
            'username': self.username,
            'password': self.password,
            'pin': self.pin,
            'billing_username': os.getenv('SIGNBOX_BILLING_USERNAME'),
            'billing_password': os.getenv('SIGNBOX_BILLING_PASSWORD'),
            'img_bookmark': 'uanataca',
            'img_name': 'uanataca.argb'
        }

    def upload_file(self, upload_file):
        url = f"{self.api_url}/sign"
        filename = upload_file.split("/")[-1].split(".")[0]
        self.payload.update(dict(
            url_in=upload_file,
            url_out=f'{SERVER_PROJECT}/result_{filename}'
        ))
        return self.session.post(
            url, data=self.payload
        )
