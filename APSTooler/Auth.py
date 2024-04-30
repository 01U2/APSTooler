"""
Documentation
The auth module provides functionalities to authenticate with the Autodesk Forge platform using the 2-legged OAuth authentication flow. 
This module is designed to obtain an access token required for making authenticated requests to the Autodesk Forge API endpoints.
"""

import os
import requests
from .Token import Token


class Auth:
    def __init__(self, client_id=None, client_secret=None):
        if client_id and client_secret:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self.client_id = os.environ.get('APS_CLIENT_ID')
            self.client_secret = os.environ.get('APS_CLIENT_SECRET')

    def auth2leg(self) -> Token:
        Host = "https://developer.api.autodesk.com"
        url = "/authentication/v2/token"
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "data:read"
        }
        response = requests.post(Host + url, data=body)
        if response.status_code != 200:
            raise Exception(response.content)
        content = response.json()
        access_token = content['access_token']
        expires_in = content['expires_in']
        token_type = content['token_type']
        result = Token(access_token, token_type, expires_in)
        return result
