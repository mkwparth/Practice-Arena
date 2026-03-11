import secrets

def create_refresh_token():
    return secrets.token_urlsafe(64)