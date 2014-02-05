""" Handle EBS volumes """
import logging

from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS

logger = logging.getLogger(__name__)


def get_watched_volumes(connection):
    """ Get a list of volumes that we are watching

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :returns: [boto.ec2.volume.Volume] -- List of volumes
    """
    return connection.get_all_volumes(
        filters={'tag-key': 'AutomatedEBSSnapshots'})


def list(connection):
    """ List watched EBS volumes

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :returns: None
    """
    volumes = get_watched_volumes(connection)

    if not volumes:
        logger.info('No watched volumes found')
        return

    logger.info('---------------+--------------+-------------')
    logger.info('{volume:<14} | {interval:<12} | {retention:<10}'.format(
        volume='Volume ID',
        interval='Interval',
        retention='Retention'))
    logger.info('---------------+--------------+-------------')

    for volume in volumes:
        if 'AutomatedEBSSnapshots' not in volume.tags:
            interval = 'Interval tag not found'
        elif volume.tags['AutomatedEBSSnapshots'] not in VALID_INTERVALS:
            interval = 'Invalid interval'
        else:
            interval = volume.tags['AutomatedEBSSnapshots']

        if 'AutomatedEBSSnapshotsRetention' not in volume.tags:
            retention = 0
        else:
            retention = volume.tags['AutomatedEBSSnapshotsRetention']

        logger.info(
            '{volume_id:<14} | {interval:<12} | {retention:<10}'.format(
                volume_id=volume.id,
                interval=interval,
                retention=retention))

    logger.info('---------------+--------------+-------------')


def unwatch(connection, volume_id):
    """ Remove watching of a volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume_id: str
    :param volume_id: VolumeID to add to the watchlist
    :returns: bool - True if the watch was successful
    """
    try:
        volume = connection.get_all_volumes(volume_ids=[volume_id])[0]
        volume.remove_tag('AutomatedEBSSnapshots')
    except KeyError:
        pass

    logger.info('Removed {} from the watchlist'.format(volume_id))

    return True


def watch(connection, volume_id, interval='daily', retention=0):
    """ Start watching a new volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume_id: str
    :param volume_id: VolumeID to add to the watchlist
    :type interval: str
    :param interval: Backup interval [hourly|daily|weekly|monthly|yearly]
    :type retention: int
    :param retention: Number of snapshots to keep. 0 == keep all
    :returns: bool - True if the watch was successful
    """
    try:
        volume = connection.get_all_volumes(volume_ids=[volume_id])[0]
    except KeyError:
        logger.warning('Volume {} not found'.format(volume_id))
        return False

    if interval not in VALID_INTERVALS:
        logger.warning(
            '{} is not a valid interval. Valid intervals are {}'.format(
                interval, ', '.join(VALID_INTERVALS)))

    # Remove the tag first
    volume.remove_tag('AutomatedEBSSnapshots')

    # Re-add the tag
    volume.add_tag('AutomatedEBSSnapshots', value=interval)

    # Remove the tag first
    volume.remove_tag('AutomatedEBSSnapshotsRetention')

    # Re-add the tag
    volume.add_tag('AutomatedEBSSnapshotsRetention', value=int(retention))

    logger.info('Updated the rotation interval to {} for {}'.format(
        interval, volume_id))

    return True
