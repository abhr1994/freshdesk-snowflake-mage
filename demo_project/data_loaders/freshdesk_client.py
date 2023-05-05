import logging.config
import os
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry
import urllib3
from demo_project.data_loaders import local_configurations
from demo_project.data_loaders.errors import *
from demo_project.data_loaders.utils import Utils

urllib3.disable_warnings()


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = local_configurations.REQUEST_TIMEOUT_IN_SEC
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def initialise_http_client():
    retries = Retry(total=local_configurations.MAX_RETRIES, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504])
    http = requests.Session()
    adapter = TimeoutHTTPAdapter(max_retries=retries)
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


class FreshdeskClient(object):
    def __init__(self, freshdesk_domain: str, api_key: str):
        self.api_key = api_key
        self._api_prefix = "https://{}/api/v2/".format(freshdesk_domain.rstrip("/"))
        self.http = initialise_http_client()
        self.utils = Utils(self)
        log_path = Path(local_configurations.LOG_LOCATION)
        if os.path.isdir(log_path.parent.absolute()):
            logging.basicConfig(filename=local_configurations.LOG_LOCATION, filemode='w',
                                format='%(asctime)s - %(module)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s',
                                level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        else:
            logging.basicConfig(
                format='%(asctime)s - %(module)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s',
                level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('fd_sdk_logs')

    def _action(self, req):
        try:
            j = req.json()
        except ValueError:
            j = {}

        error_message = "Freshdesk Request Failed"
        if "errors" in j:
            error_message = "{}: {}".format(j.get("description"), j.get("errors"))
        elif "message" in j:
            error_message = j["message"]

        if req.status_code == 400:
            raise FreshdeskBadRequest(error_message)
        elif req.status_code == 401:
            raise FreshdeskUnauthorized(error_message)
        elif req.status_code == 403:
            raise FreshdeskAccessDenied(error_message)
        elif req.status_code == 404:
            raise FreshdeskNotFound(error_message)
        elif req.status_code == 429:
            raise FreshdeskRateLimited(
                "429 Rate Limit Exceeded: API rate-limit has been reached until {} seconds. See "
                "http://freshdesk.com/api#ratelimit".format(req.headers.get("Retry-After"))
            )
        elif 500 < req.status_code < 600:
            raise FreshdeskServerError("{}: Server Error".format(req.status_code))

        # Catch any other errors
        try:
            req.raise_for_status()
        except HTTPError as e:
            raise FreshdeskBaseError("{}: {}".format(e, j))

        return j

    def call_api(self, method, url, data=None):
        response = None
        auth = HTTPBasicAuth(self.api_key, 'x')
        if method.upper() == "GET":
            self.logger.info(f"Calling {url}")
            response = self.http.get(url, auth=auth,
                                     timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                     verify=False, data=data)
        elif method.upper() == "POST":
            self.logger.info(f"Calling {url}")
            response = self.http.post(url, auth=auth, json=data,
                                      timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
        elif method.upper() == "PUT":
            self.logger.info(f"Calling {url}")
            response = self.http.put(url, auth=auth, json=data,
                                     timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
        elif method.upper() == "PATCH":
            self.logger.info(f"Calling {url}")
            response = self.http.patch(url, auth=auth, json=data,
                                       timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC, verify=False)
        elif method.upper() == "DELETE":
            self.logger.info(f"Calling {url}")
            response = self.http.delete(url, auth=auth, timeout=local_configurations.REQUEST_TIMEOUT_IN_SEC,
                                        verify=False)

        return self._action(response)
