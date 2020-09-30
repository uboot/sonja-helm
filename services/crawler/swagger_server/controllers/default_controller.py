import connexion
import six

from swagger_server import util
from swagger_server import crawler


def process_repos():  # noqa: E501
    """scan repos for new commits

     # noqa: E501


    :rtype: None
    """

    crawler.run()
    return 'success'
