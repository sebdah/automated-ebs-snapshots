""" Automatic AWS EBS snapshot handling """
import argparse
import logging
import logging.config

from automated_ebs_snapshots import config_parser
from automated_ebs_snapshots import connection_manager

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format':
            '%(asctime)s - auto-ebs - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'lib.bundle_manager': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lib.config_handler': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lib.connection_handler': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lib.deployment_manager': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
})
logger = logging.getLogger(__name__)


def main():
    """ Main function """
    parser = argparse.ArgumentParser(
        description='Automatic AWS EBS snapshot handling')
    parser.add_argument(
        '-c', '--config',
        required=True,
        help='Path to the configuration file')
    args = parser.parse_args()

    # Read configuration
    config = config_parser.get_configuration(args.config)

    # Connect to AWS
    connection = connection_manager.connect_to_ec2(
        config['aws-access-key-id'],
        config['aws-secret-access-key'],
        config['aws-region'])

    for volume in config['volumes']:
        ensure_snapshots(connection, volume)

def ensure_snapshots(connection, volume):
    """ Ensure that we have snapshots for a given volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume: str
    :param volume: AWS volume name
    """
    snapshots = connection.get_all_snapshots(
        filters={
            'volume-id': volume,
            'tag:SkymillAutoEBS': 'true'
        })


