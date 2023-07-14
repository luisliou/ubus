import requests
import json
import yaml


class Ubus:
    base_url = None
    token = None
    config_json = None

    def __init__(self, url=None, config_file=None):
        if url is not None:
            self.base_url = url
        else:
            if config_file is not None:
                with open(config_file, 'r') as file:
                    self.config_json = yaml.safe_load(file)
                self.base_url = self.config_json['global']['base_url']

    def login(self, username=None, password=None):
        if username is None:
            username = self.config_json['global']['user']
        if password is None:
            password = self.config_json['global']['password']
        url = self.base_url + '/ubus'  # Ubus API URL of your OpenWrt router
        headers = {'Content-Type': 'application/json'}
        data = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'call',
            'params': [
                "00000000000000000000000000000000",
                'session',
                'login',
                {'username': username, 'password': password}
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                for result_item in result['result']:
                    if isinstance(result_item, dict) and 'ubus_rpc_session' in result_item:
                        session_id = result_item['ubus_rpc_session']
                        self.token = session_id
                        return True
            else:
                print('Login failed')
        else:
            print('Login failed')
        return False

    def call_ubus(self, namespace, function, arguments):
        if self.token is None:
            print("Not logged in")
            return
        url = self.base_url + '/ubus'  # Ubus API URL of your OpenWrt router
        headers = {'Content-Type': 'application/json'}
        data = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'call',
            'params': [self.token, namespace, function, arguments]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                return result['result']  # Return the ubus call result
            else:
                print('Call failed')
        else:
            print('Call failed')
        return None

    def logout(self):
        url = self.base_url + '/ubus'  # Ubus API URL of your OpenWrt router
        headers = {'Content-Type': 'application/json'}
        data = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'call',
            'params': [
                self.token,
                'session',
                'destroy',
                {},
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            if 'result' in result and result['result'][0] == 0:
                self.token = None
                return
        print('Logout failed')
