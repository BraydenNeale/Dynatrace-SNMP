import json
import logging
from pprint import pprint
from snmp.host_resource_mib import HostResourceMIB
from snmp.if_mib import IFMIB

"""
Test script designed to match the flow of custom_snmp_base_plugin_remote.py
Used to test snmp classes without requiring a build/package of the extension
Usage python test.py
"""
def test_query():
    with open('properties.json') as fp:
        config = json.load(fp)

    device = _validate_device(config)
    authentication = _validate_authentication(config)

    hr_mib = HostResourceMIB(device, authentication)
    _display_metrics(hr_mib.poll_metrics())

    if_mib = IFMIB(device, authentication)
    _display_metrics(if_mib.poll_metrics())

def _display_metrics(metric_dict):
    #pprint(metric_dict)
    for endpoint,metrics in metric_dict.items():
        if isinstance(metrics, list):
            for metric in metrics:
                for name,value in metric.items():
                    print('{}: {} = {}'.format(endpoint, name, value))
        else:
            print('{} = {}'.format(endpoint, metrics))


def _validate_device(config):
    hostname = config.get('hostname')
    group_name = config.get('group')
    device_type = config.get('device_type')

    # Default port
    port = 161
    # If entered as 127.0.0.1:1234, extract the ip and the port
    split_host = hostname.split(':')
    if len(split_host) > 1:
        hostname = split_host[0]
        port = split_host[1]

    # Check inputs are valid...

    device = {
        'host': hostname,
        'port': int(port)
    }

    return device

def _validate_authentication(config):
    snmp_version = config.get('snmp_version')
    snmp_user = config.get('snmp_user')
    auth_protocol = config.get('auth_protocol', None)
    auth_key = config.get('auth_key', None)
    priv_protocol = config.get('priv_protocol', None)
    priv_key = config.get('priv_key', None)

    # Check inputs are valid...

    authentication = {
        'version': int(snmp_version),
        'user': snmp_user,
        'auth': {
            'protocol': auth_protocol,
            'key': auth_key
        },
        'priv': {
            'protocol': priv_protocol,
            'key': priv_key
        }
    }

    return authentication

if __name__ == '__main__':
    logging.basicConfig(filename='test.log',level=logging.DEBUG)
    test_query()