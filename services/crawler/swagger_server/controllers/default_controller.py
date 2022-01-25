from sonja.crawler import Crawler
from sonja.config import app
from sonja.client import scheduler


crawler = Crawler(scheduler)
logger = app.app.logger


def ping():  # noqa: E501
    """ping the service

     # noqa: E501


    :rtype: None
    """
    return 'success'

def process_repo(repo_id):  # noqa: E501
    """scan repos for new commits

     # noqa: E501


    :rtype: None
    """
    crawler.post_repo(repo_id)
    crawler.trigger()
    return 'success'
