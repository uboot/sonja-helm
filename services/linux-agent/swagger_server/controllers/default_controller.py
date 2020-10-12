import connexion
import six

from conanci import linux_agent
from conanci.config import app
from swagger_server import util

logger = app.app.logger


def ping():  # noqa: E501
    """ping the service

     # noqa: E501


    :rtype: None
    """
    return 'success'

def process_builds():  # noqa: E501
    """Process new builds

     # noqa: E501


    :rtype: None
    """
    logger.info('process builds')
    linux_agent.process_builds()
    return 'success'
