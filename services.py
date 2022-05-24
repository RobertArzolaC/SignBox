from dataclasses import dataclass

import requests


@dataclass
class SignBox:
    url = "https://signbox.developers.uanataca.com/api/sign"
    url_job = "https://signbox.developers.uanataca.com/api/job/"
    payload = {
        'url_out': 'http://localhost:5000/url-out',
        'urlback': 'http://localhost:5000/url-back',
        'env': 'test',
        'format': 'pades',
        'username': '5096707',
        'password': '7pm37Jaj',
        'pin': 'Aideartur01',
        'level': 'BES',
        'billing_username': 'jimysanchez@bit4id.pe',
        'billing_password': 'aideartur01',
        'tsa_bookmark': 'uanataca',
        'reason': 'Prueba firma',
        'location': 'Lima, Peru'
    }

    def upload_file(self, upload_data):
        files = {
            'file': upload_data.stream._file
        }
        return requests.post(self.url, files=files, data=self.payload)

    def load_job(self, job_id):
        return requests.get(f"{self.url_job}{job_id}")
