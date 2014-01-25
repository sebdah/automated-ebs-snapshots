""" Automatic AWS EBS snapshot handling """
import argparse

from automated_ebs_snapshots import connection_manager
from automated_ebs_snapshots import volume_manager


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
    actions_ag = parser.add_argument_group(
        title='Actions')
    actions_ag.add_argument(
        '--add',
        metavar='VOLUME_ID',
        help=(
            'Add a new EBS volume to the watch list. '
            'Usage: --add vol-12345678'))
    actions_ag.add_argument(
        '--list',
        action='count',
        help='List volumes that we are watching')
    args = parser.parse_args()

    # Connect to AWS
    connection = connection_manager.connect_to_ec2(
        args.region,
        args.access_key_id,
        args.secret_access_key)

    if args.list:
        volume_manager.list_watched_volumes(connection)
