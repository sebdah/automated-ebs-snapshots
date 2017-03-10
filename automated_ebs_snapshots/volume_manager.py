# -*- coding: utf-8 -*-
""" Handle EBS volumes """
import logging
import re

from boto.exception import EC2ResponseError

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

    logger.info(
        '+-----------------------'
        '+----------------------'
        '+--------------'
        '+------------+')
    logger.info(
        '| {volume:<21} '
        '| {volume_name:<20.20} '
        '| {interval:<12} '
        '| {retention:<10} |'.format(
            volume='Volume ID',
            volume_name='Volume name',
            interval='Interval',
            retention='Retention'))
    logger.info(
        '+-----------------------'
        '+----------------------'
        '+--------------'
        '+------------+')

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

        # Get the volume name
        try:
            volume_name = volume.tags['Name']
        except KeyError:
            volume_name = ''

        logger.info(
            '| {volume_id:<14} '
            '| {volume_name:<20.20} '
            '| {interval:<12} '
            '| {retention:<10} |'.format(
                volume_id=volume.id,
                volume_name=volume_name,
                interval=interval,
                retention=retention))

    logger.info(
        '+-----------------------'
        '+----------------------'
        '+--------------'
        '+------------+')


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
    except EC2ResponseError:
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
    except EC2ResponseError:
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


def get_volume_id(connection, volume):
    """
    Get Volume ID from the given volume. Input can be volume id
    or its Name tag.

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume: str
    :param volume: Volume ID or Volume Name
    :returns: Volume ID or None if the given volume does not exist
    """
    # Regular expression to check whether input is a volume id
    volume_id_pattern = re.compile('vol-\w{8}')

    if volume_id_pattern.match(volume):
        # input is volume id
        try:
            # Check whether it exists
            connection.get_all_volumes(volume_ids=[volume])
            volume_id = volume
        except EC2ResponseError:
            logger.warning('Volume {} not found'.format(volume))
            return None
    else:
        # input is volume name
        name_filter = {'tag-key': 'Name', 'tag-value': volume}
        volumes = connection.get_all_volumes(filters=name_filter)
        if not volumes:
            logger.warning('Volume {} not found'.format(volume))
            return None
        if len(volumes) > 1:
            logger.warning('Volume {} not unique'.format(volume))
        volume_id = volumes[0].id

    return volume_id


def watch_from_file(connection, file_name):
    """ Start watching a new volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type file_name: str
    :param file_name: path to config file
    :returns: None
    """
    with open(file_name, 'r') as filehandle:
        for line in filehandle.xreadlines():
            volume, interval, retention = line.rstrip().split(',')
            watch(
                connection,
                get_volume_id(connection, volume),
                interval, retention)


def unwatch_from_file(connection, file_name):
    """ Start watching a new volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type file_name: str
    :param file_name: path to config file
    :returns: None
    """
    with open(file_name, 'r') as filehandle:
        for line in filehandle.xreadlines():
            volume, interval, retention = line.rstrip().split(',')
            unwatch(connection, get_volume_id(connection, volume))


def list_snapshots(connection, volume):
    """ List all snapshots for the volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume: str
    :param volume: Volume ID or Volume Name
    :returns: None
    """

    logger.info(
        '+----------------'
        '+----------------------'
        '+---------------------------+')
    logger.info(
        '| {snapshot:<14} '
        '| {snapshot_name:<20.20} '
        '| {created:<25} |'.format(
            snapshot='Snapshot ID',
            snapshot_name='Snapshot name',
            created='Created'))
    logger.info(
        '+----------------'
        '+----------------------'
        '+---------------------------+')

    vid = get_volume_id(connection, volume)
    if vid:
        vol = connection.get_all_volumes(volume_ids=[vid])[0]
        for snap in vol.snapshots():
            logger.info(
                '| {snapshot:<14} '
                '| {snapshot_name:<20.20} '
                '| {created:<25} |'.format(
                    snapshot=snap.id,
                    snapshot_name=snap.tags.get('Name', ''),
                    created=snap.start_time))

    logger.info(
        '+----------------'
        '+----------------------'
        '+---------------------------+')
