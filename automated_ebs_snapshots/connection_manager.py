""" Handles connections to AWS """
from boto import ec2


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
    if access_key:
        connection = ec2.connect_to_region(
            region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)
    else:
        connection = ec2.connect_to_region(region)

    return connection
