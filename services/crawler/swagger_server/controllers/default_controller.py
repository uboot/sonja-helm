import connexion
import six

from swagger_server import util
from swagger_server import crawler
import swagger_client

scheduler = swagger_client.DefaultApi(swagger_client.ApiClient(None))


def process_repos():  # noqa: E501
    """scan repos for new commits

     # noqa: E501


    :rtype: None
    """
    if crawler.process_repos():
        scheduler.process_commits()
    return 'success'
