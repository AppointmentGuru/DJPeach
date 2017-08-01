import requests

class AppointmentGuru:
    url = 'https://api.appointmentguru.co'
    def __init__(self, token):
        self.token = token

    def me(self):

        headers = { 'authorization': 'Token {}'.format(self.token) }
        url = '{}/api/v2/practitioner/me/'.format(self.url)
        return requests.get(url, headers=headers)

"""
from copyandpay.appointmentguru import AppointmentGuru
guru = AppointmentGuru('...')
me=guru.me()
"""