from __future__ import print_function
import sys
from flask import Blueprint, g
from flask_httpauth import HTTPBasicAuth
import config
import requests
from urlparse import urljoin
import os

token = Blueprint('token', __name__)
auth = HTTPBasicAuth()


def url_join(base, port, url, *urls):
    return urljoin(base + ":" + port, os.path.join(url, *urls))


@auth.verify_password
def verify_password(username, password):
    params = {
        'auth': {
            'tenantName': config.TENANT_NAME,
            'passwordCredentials': {
                'username': username,
                'password': password
            }
        }
    }
    url = url_join(config.HOST, config.PORT_TOKEN, config.VER_TOKEN, 'tokens')
    res = requests.post(url, json=params)
    print (url, file=sys.stderr)
    print (params, file=sys.stderr)
    print (res.status_code, file=sys.stderr)
    print (res.content, file=sys.stderr)
    if res.status_code == 200:
        g.token = res.content
        return True
    return False
