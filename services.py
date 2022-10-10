from datetime import datetime
import os
import requests

from constants import BASE_API


SERVER_PROJECT = os.getenv("SERVER_PROJECT", "uanataca")


class SignBox:
    api_url = BASE_API

    def __init__(self, username, password, pin):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.pin = pin
        self.build_payload()
        
    def build_payload(self, **kwargs):
        self.payload = {
            'urlback': f'{SERVER_PROJECT}/url-back',
            'url_out': f'{SERVER_PROJECT}/url-out',
            'env': 'test',
            'format': 'pades',
            'username': self.username,
            'password': self.password,
            'pin': self.pin,
            'level': 'BES',
            'billing_username': os.getenv('SIGNBOX_BILLING_USERNAME'),
            'billing_password': os.getenv('SIGNBOX_BILLING_PASSWORD'),
            'reason': 'Prueba firma',
            'location': 'Lima, Peru'
        }

    def upload_file(self, upload_data):
        url = f"{self.api_url}/sign"
        files = dict(file_in=upload_data.stream._file)
        return self.session.post(url, files=files, data=self.payload)
