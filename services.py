import os
import requests

from constants import BASE_API


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
            'url_out': 'http://localhost:5000/url-out',
            'urlback': 'http://localhost:5000/url-back',
            'env': 'test',
            'format': 'pades',
            'username': self.username,
            'password': self.password,
            'pin': self.pin,
            'level': 'BES',
            'billing_username': os.getenv('SIGNBOX_BILLING_USERNAME'),
            'billing_password': os.getenv('SIGNBOX_BILLING_PASSWORD'),
            'tsa_bookmark': 'uanataca',
            'reason': 'Prueba firma',
            'location': 'Lima, Peru'
        }

    def upload_file(self, upload_data):
        url = f"{self.api_url}/sign"
        files = dict(file=upload_data.stream._file)
        return self.session.post(url, files=files, data=self.payload)

    def load_job(self, job_id):
        url = f"{self.api_url}/job/{job_id}"
        return self.session.get(url)
