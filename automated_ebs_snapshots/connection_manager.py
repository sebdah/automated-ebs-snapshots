""" Handles connections to AWS """
import logging
import sys

from boto import ec2

logger = logging.getLogger(__name__)


def connect_to_ec2(region='us-east-1', access_key=None, secret_key=None):
    """ Connect to AWS ec2

    :type region: str
    :param region: AWS region to connect to
    :type access_key: str
    :param access_key: AWS access key id
    :type secret_key: str
    :param secret_key: AWS secret access key
    :returns: boto.ec2.connection.EC2Connection -- EC2 connection
    """
    logger.info('Connecting to AWS EC2 in {}'.format(region))
    if access_key:
        connection = ec2.connect_to_region(
            region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)
    else:
        connection = ec2.connect_to_region(region)

    if not connection:
        logger.error('An error occurred when connecting to EC2')
        sys.exit(1)

    return connection
