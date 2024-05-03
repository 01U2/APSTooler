"""
## Disclaimer

The APSTooler ("the toolkit") is provided without any warranties. Its use is at your own risk, and the creator accepts no liability for any damages arising from its use. The toolkit is for informational purposes only and should not be considered professional advice. By using the toolkit, you agree to indemnify the creator against any claims or damages. If you do not agree, please refrain from using the toolkit.
"""


class Token():
    def __init__(self, access_token, token_type, expires_in, refresh_token=None):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token

    def is_expired(self) -> bool:
        return self.expires_in <= 0