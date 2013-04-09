__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

from tcapy.tcapy import encode_parameter_pairs, encode_custom_parameters, encode_action_parameters
import unittest
import urllib
import urlparse

class TestEncodeParameterPairs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = 'test_key'
        cls.value = 'test_value'
        cls.pair = {cls.key: cls.value}
        cls.prefix = 'test_prefix.'

    def test_none_params_raises_exception(self):
        self.assertRaises(Exception, encode_parameter_pairs, None)

    def test_empty_params_returns_empty_string(self):
        assert encode_parameter_pairs({}) == ''

    def test_starts_with_name(self):
        assert encode_parameter_pairs(self.pair).startswith('name')

    def test_contains_ampersand(self):
        assert '&' in encode_parameter_pairs(self.pair)

    def test_prefix_default(self):
        key, value = urlparse.parse_qsl(encode_parameter_pairs(self.pair))
        assert ('name', self.key) == key
        assert ('value', self.value) == value

    def test_prefix_defined(self):
        key, value = urlparse.parse_qsl(encode_parameter_pairs(self.pair, prefix=self.prefix))
        assert ('name', self.prefix + self.key) == key
        assert ('value', self.value) == value


class TestEncodeCustomParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_key, cls.config_value = 'config_key', 'config_value'
        cls.system_key, cls.system_value = 'system_key', 'system_value'
        cls.env_key, cls.env_value = 'env_key', 'env_value'
        cls.config = {cls.config_key: cls.config_value}
        cls.system = {cls.system_key: cls.system_value}
        cls.env = {cls.env_key: cls.env_value}

    def test_none_params_raises_exception(self):
        self.assertRaises(Exception, encode_custom_parameters, None)

    def test_empty_params_returns_empty_string(self):
        assert encode_custom_parameters(**{}) == ''

    def test_valid_config_parameters_have_no_prefix(self):
        key, value = urlparse.parse_qsl(encode_custom_parameters(**{'config': self.config}))
        assert ('name', self.config_key) == key
        assert ('value', self.config_value) == value

    def test_valid_system_parameters_have_prefix(self):
        prefix = 'system.'
        key, value = urlparse.parse_qsl(encode_custom_parameters(**{'system': self.system}))
        assert ('name', prefix + self.system_key) == key
        assert ('value', self.system_value) == value

    def test_valid_env_parameters_have_prefix(self):
        prefix = 'env.'
        key, value = urlparse.parse_qsl(encode_custom_parameters(**{'env': self.env}))
        assert ('name', prefix + self.env_key) == key
        assert ('value', self.env_value) == value


class TestEncodeActionParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_id = '1234'
        cls.modification_id = '42'
        cls.top = True
        cls.agent_1 = '12'
        cls.agent_2 = '13'
        cls.agents = [cls.agent_1, cls.agent_2]
        cls.config_key, cls.config_value = 'config_key', 'config_value'
        cls.system_key, cls.system_value = 'system_key', 'system_value'
        cls.env_key, cls.env_value = 'env_key', 'env_value'
        cls.config = {cls.config_key: cls.config_value}
        cls.system = {cls.system_key: cls.system_value}
        cls.env = {cls.env_key: cls.env_value}

    def test_empty_params_returns_build_string(self):
        assert encode_action_parameters(self.build_id, **{}) == 'add2Queue={0}'.format(self.build_id)

    def test_modification_id(self):
        encoded = encode_action_parameters(self.build_id, **{'modification_id': self.modification_id})
        mod_id, build_id = urlparse.parse_qsl(encoded)
        assert ('modificationId', self.modification_id) == mod_id
        assert ('add2Queue', self.build_id) == build_id

    def test_move_to_top(self):
        encoded = encode_action_parameters(self.build_id, **{'top': self.top})
        top, build_id = urlparse.parse_qsl(encoded)
        assert ('moveToTop', str(True)) == top
        assert ('add2Queue', self.build_id) == build_id

    def test_single_agent(self):
        encoded = encode_action_parameters(self.build_id, **{'agents': self.agent_1})
        agent, build_id = urlparse.parse_qsl(encoded)
        assert ('agentId', str(self.agent_1)) == agent
        assert ('add2Queue', self.build_id) == build_id

    def test_multiple_agents(self):
        encoded = encode_action_parameters(self.build_id, **{'agents': [self.agent_1, self.agent_2]})
        agent_1, agent_2, build_id = urlparse.parse_qsl(encoded)
        assert ('agentId', str(self.agent_1)) == agent_1
        assert ('agentId', str(self.agent_2)) == agent_2
        assert ('add2Queue', self.build_id) == build_id

    @unittest.skip('Not Implemented.')
    def test_all_compatible_agents(self):
        pass

    def test_config_parameters(self):
        encoded = encode_action_parameters(self.build_id, **{'config': self.config})
        build_id, key, value = urlparse.parse_qsl(encoded)
        assert ('name', self.config_key) == key
        assert ('value', self.config_value) == value
        assert ('add2Queue', self.build_id) == build_id

    def test_system_parameters(self):
        prefix = 'system.'
        encoded = encode_action_parameters(self.build_id, **{'system': self.system})
        build_id, key, value = urlparse.parse_qsl(encoded)
        assert ('name', prefix + self.system_key) == key
        assert ('value', self.system_value) == value
        assert ('add2Queue', self.build_id) == build_id

    def test_env_parameters(self):
        prefix = 'env.'
        encoded = encode_action_parameters(self.build_id, **{'env': self.env})
        build_id, key, value = urlparse.parse_qsl(encoded)
        assert ('name', prefix + self.env_key) == key
        assert ('value', self.env_value) == value
        assert ('add2Queue', self.build_id) == build_id

class TestTeamCityApi(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()