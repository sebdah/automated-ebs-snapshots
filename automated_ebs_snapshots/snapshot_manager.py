""" Module handling the snapshots """

CONNECTION = None


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
