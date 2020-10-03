import connexion
import six

from swagger_server import util
from swagger_server.config import app

logger = app.app.logger


def process_builds():  # noqa: E501
    """Process new builds

     # noqa: E501


    :rtype: None
    """
    logger.info('process builds')
    return 'do some magic!'
