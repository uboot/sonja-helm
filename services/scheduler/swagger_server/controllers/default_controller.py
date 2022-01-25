from sonja.scheduler import Scheduler
from sonja.config import app
from sonja.client import linux_agent, windows_agent

logger = app.app.logger

scheduler = Scheduler(linux_agent, windows_agent)


def ping():  # noqa: E501
    """ping the service

     # noqa: E501


    :rtype: None
    """
    return 'success'

def process_commits():  # noqa: E501
    """Process new commits

     # noqa: E501


    :rtype: None
    """
    scheduler.trigger()
    return 'success'

def process_packages():  # noqa: E501
    """Process new packages

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
