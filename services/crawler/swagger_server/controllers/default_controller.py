import connexion
import six

from conanci import crawler
from conanci.config import app
import swagger_client
from swagger_server import util

logger = app.app.logger
scheduler = swagger_client.DefaultApi(swagger_client.ApiClient(None))


def process_repos():  # noqa: E501
    """scan repos for new commits

     # noqa: E501


    :rtype: None
    """
    if crawler.process_repos():
        logger.info('trigger scheduler: process commits')
        scheduler.process_commits()
    return 'success'
