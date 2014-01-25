""" Handle EBS volumes """
from automated_ebs_snapshots.valid_intervals import VALID_INTERVALS


def list_watched_volumes(connection):
    """ List watched EBS volumes

    :type connection: boto.ec2.connection.EC2Connection
    :param connection: EC2 connection object
    :returns: None
    """
    volumes = connection.get_all_volumes(
        filters={
            'tag-key': 'SkymillEBSSnapshotInterval'
        })

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
