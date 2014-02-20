""" Automatic AWS EBS snapshot handling """
import logging
import logging.config
import time
import sys

from automated_ebs_snapshots.command_line_options import args
from automated_ebs_snapshots import config_file_parser
from automated_ebs_snapshots import connection_manager
from automated_ebs_snapshots import snapshot_manager
from automated_ebs_snapshots import volume_manager
from automated_ebs_snapshots.daemon import Daemon

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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': args.log_file,
            'when': 'midnight',
            'backupCount': 5
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'lib.bundle_manager': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lib.config_handler': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lib.connection_handler': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'lib.deployment_manager': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
})
logger = logging.getLogger(__name__)


class AutoEBSDaemon(Daemon):
    """ Daemon for automatic-ebs-snapshots"""

    def run(self, check_interval=300):
        """ Run the daemon

        :type check_interval: int
        :param check_interval: Delay in seconds between checks
        """
        while True:
            # Read configuration from the config file if present, else fall
            # back to command line options
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

            snapshot_manager.run(connection)

            logger.info('Sleeping {} seconds until next check'.format(
                check_interval))
            time.sleep(check_interval)


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

    if args.daemon:
        pid_file = '/tmp/automatic-ebs-snapshots.pid'
        daemon = AutoEBSDaemon(pid_file)

        if args.daemon == 'start':
            daemon.start()

        elif args.daemon == 'stop':
            daemon.stop()
            sys.exit(0)

        elif args.daemon == 'restart':
            daemon.restart()

        elif args.daemon in ['foreground', 'fg']:
            daemon.run()

        else:
            print 'Valid options for --daemon are start, stop and restart'
            sys.exit(1)

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
