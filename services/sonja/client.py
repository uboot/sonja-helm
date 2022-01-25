import os

from sonja.swagger_client import AgentApi, ApiClient, Configuration, SchedulerApi
from urllib3.exceptions import MaxRetryError
from sonja.swagger_client.rest import ApiException

linux_agent_url = os.environ.get('SONJA_LINUXAGENT_URL', '127.0.0.1')
linux_agent_configuration = Configuration()
linux_agent_configuration.host = "http://{0}:8080".format(linux_agent_url)
linux_agent = AgentApi(ApiClient(linux_agent_configuration))

windows_agent_url = os.environ.get('SONJA_WINDOWSAGENT_URL', '127.0.0.1')
windows_agent_configuration = Configuration()
windows_agent_configuration.host = "http://{0}:8080".format(windows_agent_url)
windows_agent = AgentApi(ApiClient(windows_agent_configuration))

scheduler_url = os.environ.get('SONJA_SCHEDULER_URL', '127.0.0.1')
configuration = Configuration()
configuration.host = "http://{0}:8080".format(scheduler_url)
scheduler = SchedulerApi(ApiClient(configuration))
