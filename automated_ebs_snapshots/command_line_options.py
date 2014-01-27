""" Command line options """
import argparse

from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS

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
    help='AWS region')
general_ag = parser.add_argument_group(
    title='General')
general_ag.add_argument(
    '-c', '--config',
    help='Configuration file to read')
general_ag.add_argument(
    '-i', '--interval',
    default='daily',
    help='Volume snapshotting interval. Valid values are: {}'.format(
        ', '.join(VALID_INTERVALS)))
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
actions_ag = parser.add_argument_group(
    title='Actions')
actions_ag.add_argument(
    '--run',
    action='count',
    help='Run the watcher to ensure snapshots')
args = parser.parse_args()
