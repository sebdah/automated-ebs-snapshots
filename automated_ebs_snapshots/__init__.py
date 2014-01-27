""" Automatic AWS EBS snapshot handling """
import argparse

from automated_ebs_snapshots import connection_manager
from automated_ebs_snapshots import volume_manager
from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS


def main():
    """ Main function """
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
    args = parser.parse_args()

    # Connect to AWS
    connection = connection_manager.connect_to_ec2(
        args.region,
        args.access_key_id,
        args.secret_access_key)

    if args.watch:
        volume_manager.watch(connection, args.watch, args.interval)

    if args.unwatch:
        volume_manager.unwatch(connection, args.unwatch)

    if args.list:
        volume_manager.list(connection)
