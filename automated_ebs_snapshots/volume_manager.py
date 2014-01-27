""" Handle EBS volumes """
from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS


def get_watched_volumes(connection):
    """ Get a list of volumes that we are watching

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :returns: [boto.ec2.volume.Volume] -- List of volumes
    """
    return connection.get_all_volumes(
        filters={'tag-key': 'SkymillEBSSnapshotInterval'})


def list(connection):
    """ List watched EBS volumes

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :returns: None
    """
    volumes = get_watched_volumes(connection)

    if not volumes:
        print('No watched volumes found')
        return

    print('---------------+-------------------------------')
    print('{volume:<14} | {interval:<12}'.format(
        volume='Volume ID',
        interval='Interval'))
    print('---------------+-------------------------------')

    for volume in volumes:
        if 'SkymillEBSSnapshotInterval' not in volume.tags:
            print('{volume_id:<14} | {interval:<12}'.format(
                volume_id=volume.id,
                interval='Interval tag not found'))
        elif volume.tags['SkymillEBSSnapshotInterval'] not in VALID_INTERVALS:
            print('{volume_id:<14} | {interval:<12}'.format(
                volume_id=volume.id,
                interval='Invalid interval'))
        else:
            print('{volume_id:<14} | {interval:<12}'.format(
                volume_id=volume.id,
                interval=volume.tags['SkymillEBSSnapshotInterval']))

    print('---------------+-------------------------------')


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
        volume.remove_tag('SkymillEBSSnapshotInterval')
    except KeyError:
        pass

    print('Removed {} from the watchlist'.format(volume_id))

    return True


def watch(connection, volume_id, interval='daily'):
    """ Start watching a new volume

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :type volume_id: str
    :param volume_id: VolumeID to add to the watchlist
    :type interval: str
    :param interval: Backup interval [hourly|daily|weekly|monthly|yearly]
    :returns: bool - True if the watch was successful
    """
    try:
        volume = connection.get_all_volumes(volume_ids=[volume_id])[0]
    except KeyError:
        print('Volume {} not found'.format(volume_id))
        return False

    if interval not in VALID_INTERVALS:
        print('{} is not a valid interval. Valid intervals are {}'.format(
            interval, ', '.join(VALID_INTERVALS)))

    # Remove the tag first
    volume.remove_tag('SkymillEBSSnapshotInterval')

    # Re-add the tag
    volume.add_tag('SkymillEBSSnapshotInterval', value=interval)

    print('Updated the rotation interval to {} for {}'.format(
        interval, volume_id))

    return True
