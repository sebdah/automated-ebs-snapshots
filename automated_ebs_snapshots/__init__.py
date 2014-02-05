""" Automatic AWS EBS snapshot handling """
import logging
import logging.config

from automated_ebs_snapshots.command_line_options import args
from automated_ebs_snapshots import config_file_parser
from automated_ebs_snapshots import connection_manager
from automated_ebs_snapshots import snapshot_manager
from automated_ebs_snapshots import volume_manager

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
    # Read configuration from the config file if present, else fall back to
    # command line options
    if args.config:
        config = config_file_parser.get_configuration(args.config)
        access_key_id = config['access-key-id']
        secret_access_key = config['secret-access-key']
        region = config['region']
    else:
        access_key_id = args.access_key_id
        secret_access_key = args.secret_access_key
        region = args.region

    # Connect to AWS
    connection = connection_manager.connect_to_ec2(
        region, access_key_id, secret_access_key)

    if args.watch:
        volume_manager.watch(
            connection,
            args.watch,
            args.interval,
            args.retention)

    if args.unwatch:
        volume_manager.unwatch(connection, args.unwatch)

    if args.list:
        volume_manager.list(connection)

    if args.run:
        snapshot_manager.run(connection)
