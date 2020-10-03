import connexion
import six

import swagger_client
from swagger_server import util
from swagger_server import scheduler
from swagger_server.config import app

logger = app.app.logger
linux_agent = swagger_client.DefaultApi(swagger_client.ApiClient(None))


def process_commits():  # noqa: E501
    """Process new commits

     # noqa: E501


    :rtype: None
    """
    if scheduler.process_commits():
        logger.info('trigger linux agent: process builds')
        linux_agent.process_builds()
    return 'success'

def process_packages():  # noqa: E501
    """Process new packages

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
