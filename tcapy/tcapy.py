__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

import functools
import os
import requests
import urllib

class TeamCityApiError(Exception):
    pass

def expects(expected_status_code, expected_content_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            status_code = response.status_code
            content_type = response.headers.get('content-type')
            if status_code != expected_status_code:
                raise TeamCityApiError('Got status code {0}; expected {1}.'.format(status_code, expected_status_code))
            if bool(content_type) != bool(expected_content_type) or \
                    (content_type and content_type != expected_content_type.lower()):
                raise TeamCityApiError('Got content-type {0}; expected {1}.'.format(content_type, expected_content_type))
            return response
        return wrapper
    return decorator

class TeamCityApi(object):
    SESSION_DEFAULTS = {
        'headers': {
            'accept': 'application/json'
        },
        'auth': (os.environ.get('TCAPY_USERNAME'), os.environ.get('TCAPY_PASSWORD')),
        'verify': False
    }
    def __init__(self, **kwargs):
        self.server = kwargs.pop('server', os.environ.get('TCAPY_SERVER'))
        self.config = dict(self.SESSION_DEFAULTS, **kwargs)
        self.session = requests.Session()

    @expects(200, 'text/plain')
    def version(self):
        return self.get('version', config=dict(self.config, headers=None))

    @expects(200, 'application/json')
    def projects(self, **kwargs): #paginates @ 100 (assumption)
        return self.get('projects', **kwargs)

    @expects(200, 'application/json')
    def builds(self, **kwargs): #paginates @ 100 (assertion)
        return self.get('builds', **kwargs)

    @expects(200, 'application/json')
    def configurations(self, **kwargs): #paginates @ 100 (assumption)
        return self.get('buildTypes', **kwargs)

    @expects(200, 'application/json')
    def agents(self, **kwargs):
        return self.get('agents', **kwargs)

    def get(self, *resources, **kwargs):
        config = kwargs.pop('config', self.config)
        key = build_url_filter(**kwargs)
        url = build_rest_url(self.server, resources, key)
        return self.session.get(url, **config)

    def action(self, id, **kwargs):
        config = kwargs.pop('config', self.config)
        url = build_action_url(id, **kwargs)
        return self.session.get(url, **config)

    @expects(200, None)
    def start_build(self, id, **kwargs):
        return self.action(id, kwargs)


def encode_parameter_pairs(params, prefix=''):
    return '&'.join((urllib.urlencode({'name': '{0}{1}'.format(prefix, k), 'value': v}) for k,v in params.items()))

def encode_custom_parameters(**kwargs):
    config = encode_parameter_pairs(kwargs.get('config', {}))
    system = encode_parameter_pairs(kwargs.get('system', {}), prefix='system.')
    env = encode_parameter_pairs(kwargs.get('env', {}), prefix='env.')
    return '&'.join(filter(None, (config, system, env)))

def encode_action_parameters(id, **kwargs):
    params = dict((k,v) for k,v in {'add2Queue': str(id),
                                    'modificationId': kwargs.get('modification_id', None),
                                    'moveToTop': kwargs.get('top', None),
                                    'agentId': kwargs.get('agents', None),}.items() if v)
    params = urllib.urlencode(params, doseq=True)
    return '&'.join(filter(None, (params, encode_custom_parameters(**kwargs))))

def build_action_url(server, id, **kwargs):
    return '/'.join((server, 'action.html?{0}'.format(encode_action_parameters(id, **kwargs))))

def build_rest_url(server, *resources):
    return '/'.join((server, 'app', 'rest') + filter(None, resources))

def build_url_filter(**kwargs):
    return ':'.join(next(((k, str(v)) for (k,v) in ((k, kwargs.get(k)) for k in ('id', 'name')) if v), ()))