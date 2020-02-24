""" Module handling the snapshots """
import logging
import datetime

from boto.exception import EC2ResponseError

from automated_ebs_snapshots import volume_manager
from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS

logger = logging.getLogger(__name__)


def run(connection):
    """ Ensure that we have snapshots for a given volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :returns: None
    """
    volumes = volume_manager.get_watched_volumes(connection)

    for volume in volumes:
        _ensure_snapshot(connection, volume)
        _remove_old_snapshots(connection, volume)


def _create_snapshot(volume):
    """ Create a new snapshot

    :type volume: boto.ec2.volume.Volume
    :param volume: Volume to snapshot
    :returns: boto.ec2.snapshot.Snapshot -- The new snapshot
    """
    logger.info('Creating new snapshot for {}'.format(volume.id))
    snapshot = volume.create_snapshot(
        description="Automatic snapshot by Automated EBS Snapshots")
    logger.info('Created snapshot {} for volume {}'.format(
        snapshot.id, volume.id))

    return snapshot


def _ensure_snapshot(connection, volume):
    """ Ensure that a given volume has an appropriate snapshot

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume: boto.ec2.volume.Volume
    :param volume: Volume to check
    :returns: None
    """
    if 'AutomatedEBSSnapshots' not in volume.tags:
        logger.warning(
            'Missing tag AutomatedEBSSnapshots for volume {}'.format(
                volume.id))
        return

    interval = volume.tags['AutomatedEBSSnapshots']
    if volume.tags['AutomatedEBSSnapshots'] not in VALID_INTERVALS:
        logger.warning(
            '"{}" is not a valid snapshotting interval for volume {}'.format(
                interval, volume.id))
        return

    snapshots = connection.get_all_snapshots(filters={'volume-id': volume.id})

    # Create a snapshot if we don't have any
    if not snapshots:
        _create_snapshot(volume)
        return

    min_delta = 3600*24*365*10  # 10 years :)
    for snapshot in snapshots:
        timestamp = datetime.datetime.strptime(
            snapshot.start_time,
            '%Y-%m-%dT%H:%M:%S.%fZ')
        delta_seconds = int(
            (datetime.datetime.utcnow() - timestamp).total_seconds())

        if delta_seconds < min_delta:
            min_delta = delta_seconds

    logger.info('The newest snapshot for {} is {} seconds old'.format(
        volume.id, min_delta))
    if interval == 'hourly' and min_delta > 3600:
        _create_snapshot(volume)
    elif interval == 'daily' and min_delta > 3600*24:
        _create_snapshot(volume)
    elif interval == 'weekly' and min_delta > 3600*24*7:
        _create_snapshot(volume)
    elif interval == 'monthly' and min_delta > 3600*24*30:
        _create_snapshot(volume)
    elif interval == 'yearly' and min_delta > 3600*24*365:
        _create_snapshot(volume)
    else:
        logger.info('No need for a new snapshot of {}'.format(volume.id))


def _remove_old_snapshots(connection, volume):
    """ Remove old snapshots

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume: boto.ec2.volume.Volume
    :param volume: Volume to check
    :returns: None
    """
    if 'AutomatedEBSSnapshotsRetention' not in volume.tags:
        logger.warning(
            'Missing tag AutomatedEBSSnapshotsRetention for volume {}'.format(
                volume.id))
        return
    retention = int(volume.tags['AutomatedEBSSnapshotsRetention'])

    snapshots = connection.get_all_snapshots(filters={'volume-id': volume.id})

    # Sort the list based on the start time
    snapshots.sort(key=lambda x: x.start_time)

    # Remove snapshots we want to keep
    snapshots = snapshots[:-int(retention)]

    if not snapshots:
        logger.info('No old snapshots to remove')
        return

    for snapshot in snapshots:
        logger.info('Deleting snapshot {}'.format(snapshot.id))
        try:
            snapshot.delete()
        except EC2ResponseError as error:
            logger.warning('Could not remove snapshot: {}'.format(
                error.message))

    logger.info('Done deleting snapshots')
