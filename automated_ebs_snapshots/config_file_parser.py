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

    try:
        config = {
            'access-key-id': conf.get('general', 'access-key-id'),
            'secret-access-key': conf.get('general', 'secret-access-key'),
            'region': conf.get('general', 'region'),
        }
    except NoOptionError as err:
        logger.error('Error in config file: {}'.format(err))
        sys.exit(1)

    return config
