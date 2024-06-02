from flask import request
import os

def authenticate():
    auth_token = request.headers.get('Authorization')
    # if auth_token != f'Bearer {os.environ.get("PASSWORD")}':
    if auth_token != f'Bearer 1234':
        return False
    return True