""" Command line options """
import argparse
import sys
import os.path
from ConfigParser import SafeConfigParser

from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS

settings = SafeConfigParser()
settings.read('{}/settings.conf'.format(
    os.path.dirname(os.path.realpath(__file__))))


parser = argparse.ArgumentParser(
    description='Automatic AWS EBS snapshot handling')
aws_config_ag = parser.add_argument_group(
    title='AWS configuration options')
aws_config_ag.add_argument(
    '--access-key-id',
    help='AWS access key')
aws_config_ag.add_argument(
    '--secret-access-key',
    help='AWS secret access key')
aws_config_ag.add_argument(
    '--region',
    default='us-east-1',
    help='AWS region. Default: us-east-1')
general_ag = parser.add_argument_group(
    title='General')
general_ag.add_argument(
    '-c', '--config',
    help='Configuration file to read')
general_ag.add_argument(
    '-i', '--interval',
    default='daily',
    help=(
        'Volume snapshotting interval. Default: daily. '
        'Valid values are: {}'.format(', '.join(VALID_INTERVALS))))
general_ag.add_argument(
    '-r', '--retention',
    default=0,
    type=int,
    help=(
        'Number of snapshots to keep. 0 == keep all. '
        'Default: 0. '
        'WARNING: This setting will delete older snapshots!'))
general_ag.add_argument(
    '--version',
    action='count',
    help='Print the Automated EBS Snapshots version and exit')
general_ag.add_argument(
    '--log-file',
    help='Path to file to send logs to')
general_ag.add_argument(
    '--daemon',
    help=(
        'Run Automatic EBS Snapshots in daemon mode. Valid modes are '
        '[start|stop|restart|foreground]'))
admin_actions_ag = parser.add_argument_group(
    title='Administrative actions')
admin_actions_ag.add_argument(
    '--list',
    action='count',
    help='List volumes that we are watching')
admin_actions_ag.add_argument(
    '--unwatch',
    metavar='VOLUME_ID',
    help=(
        'Remove an EBS volume from the watch list. '
        'Usage: --unwatch vol-12345678'))
admin_actions_ag.add_argument(
    '--watch',
    metavar='VOLUME_ID',
    help=(
        'Add a new EBS volume to the watch list. '
        'Usage: --watch vol-12345678'))
admin_actions_ag.add_argument(
    '--snapshots',
    metavar='VOLUME',
    help='List all snapshots of this EBS volume')
admin_actions_ag.add_argument(
    '--unwatch-file',
    metavar='FILE_NAME',
    help=(
        'Remove all EBS volumes in the config file from the watch list. '
        'Usage: --unwatch-file volumes.conf'))
admin_actions_ag.add_argument(
    '--watch-file',
    metavar='FILE_NAME',
    help=(
        'Add all EBS volumes in the config file to the watch list. '
        'Usage: --watch-file volumes.conf'))

actions_ag = parser.add_argument_group(
    title='Actions')
actions_ag.add_argument(
    '--run',
    action='count',
    help='Run the watcher to ensure snapshots')

actions_ag.add_argument(
    '--force-run',
    action='count',
    help='Similar to --run, but always take a snapshot and purge '
         'snapshots that should be removed.')

args = parser.parse_args()

if args.version:
    print('Automated EBS Snapshots version {}'.format(
        settings.get('general', 'version')))
    sys.exit(0)
