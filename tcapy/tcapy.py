__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

import functools
import os
import requests

def expects(expected_status_code, expected_content_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            status_code = response.status_code
            content_type = response.headers.get('content-type', '').lower()
            if status_code != expected_status_code:
                raise Exception('Got status code {0}; expects {1}.'.format(status_code, expected_status_code))
            if content_type != expected_content_type.lower():
                raise Exception('Got content-type {0}; expects {1}.'.format(content_type, expected_content_type))
            return response
        return wrapper
    return decorator

class TeamCityApi(object):
    DEFAULTS = {
        'headers': {
            'accept': 'application/json'
        },
        'auth': (os.environ.get('TCAPY_USERNAME'), os.environ.get('TCAPY_PASSWORD')),
        'verify': False
    }
    def __init__(self, server, **kwargs):
        self.server = server
        self.root = self.build_url('app', 'rest') #hrm
        self.config = dict(self.DEFAULTS, **kwargs)
        self.session = requests.Session()

    def build_url(self, *resources):
        return '/'.join((self.server,) + filter(None, resources))

    @expects(200, 'text/plain')
    def version(self):
        config = dict(self.config, headers=None)
        return self.session.get(self.build_url('app', 'rest', 'version'), **config)

    @expects(200, 'application/json')
    def projects(self, **kwargs): #paginates @ 100 (assumption)
        predicate = ''.join('{0}:{1}'.format(k,v) for k,v in kwargs.items() if v)
        return self.session.get(self.build_url('app', 'rest', 'projects', predicate), **self.config)

    @expects(200, 'application/json')
    def builds(self, **kwargs): #paginates @ 100 (assertion)
        predicate = ''.join('{0}:{1}'.format(k,v) for k,v in kwargs.items() if v)
        return self.session.get(self.build_url('app', 'rest', 'builds', predicate), **self.config)

    @expects(200, 'application/json')
    def configurations(self, **kwargs): #paginates @ 100 (assumption)
        predicate = ''.join('{0}:{1}'.format(k,v) for k,v in kwargs.items() if v)
        return self.session.get(self.build_url('app', 'rest', 'buildTypes', predicate), **self.config)

    def start_build(self, id):
        url = self.server + '/action.html?add2Queue={0}'.format(id)
        print url
        #return self.session.post(self.)
