import connexion
import six

from swagger_server import util
from swagger_server import scheduler


def process_commits():  # noqa: E501
    """Process new commits

     # noqa: E501


    :rtype: None
    """
    scheduler.process_commits()
    return 'success'

def process_packages():  # noqa: E501
    """Process new packages

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
