""" Configuration file parser """
import logging
import sys
from ConfigParser import SafeConfigParser, NoOptionError

logger = logging.getLogger(__name__)


def get_configuration(filename):
    """ Read configuration file

    :type filename: str
    :param filename: Path to the configuration file
    """
    logger.debug('Reading configuration from {}'.format(filename))
    conf = SafeConfigParser()
    conf.read(filename)

    if not conf:
        logger.error('Configuration file {} not found'.format(filename))
        sys.exit(1)

    if not conf.has_section('general'):
        logger.error('Missing [general] section in the configuration file')
        sys.exit(1)

    config = {
        'aws-access-key-id': conf.get('general', 'aws-access-key-id'),
        'aws-secret-access-key': conf.get('general', 'aws-secret-access-key'),
        'aws-region': conf.get('general', 'aws-region'),
        'volumes': {}
    }

    # Get all volume definitions
    for section in conf.sections():
        if section[0:4] == 'vol-':
            logger.debug('Parsing section {}'.format(section))
            try:
                config['volumes'][section] = {
                    'snapshot-interval': conf.get(
                        section, 'snapshot-interval'),
                    'snapshot-retention': conf.get(
                        section, 'snapshot-retention')
                }
            except NoOptionError as err:
                logger.error('Missing option in configuration: {}'.format(err))
                sys.exit(1)

    return config
