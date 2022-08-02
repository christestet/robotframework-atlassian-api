"""

This is a very thin wrapper for servicedesk. You can access all of servicedesk's usual
methods via SERVICEDESKLibrary calls in Robot Framework.

"""
# pylint: disable=no-value-for-parameter,unused-argument,useless-object-inheritance,broad-except,consider-iterating-dictionary
import ast

from atlassian import ServiceDesk
import wrapt
from robot.api import logger


def _str_to_data(string):
    try:
        return ast.literal_eval(str(string).strip())
    except Exception:
        return string


@wrapt.decorator
def _str_vars_to_data(function, instance, args, kwargs):
    args = [_str_to_data(arg) for arg in args]
    kwargs = dict((arg_name, _str_to_data(arg))
                  for arg_name, arg in kwargs.items())
    result = function(*args, **kwargs)
    return result


class SERVICEDESKKeywords(object):
    """
    This looks tricky but it's just the Robot Framework Hybrid Library API.
    https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#hybrid-library-api
    """

    ROBOT_LIBRARY_SCOPE = "Global"
    _servicedesk = ServiceDesk
    _session = None

    def get_keyword_names(self):
        """
        Generate List of keywords from servicedesk lib
        """
        keywords = [
            name
            for name, function in self._servicedesk.__dict__.items()
            if hasattr(function, "__call__")
        ]

        keywords.append("connect_to_servicedesk")

        return keywords

    def connect_to_servicedesk(self, url=None, username=None, password=None, **kwargs):
        """
        Connect To Servicedesk    https://localhost:443/servicedesk    user   password
        Full list of arguments https://atlassian-python-api.readthedocs.io/index.html
        Use the {session} for all your keywords
        """
        self._session = ServiceDesk(
            url=url, username=username, password=password, **kwargs)
        logger.debug("Connected to SERVICEDESK")
        return self._session

    def __getattr__(self, name):
        func = None
        if name in self._servicedesk.__dict__.keys():
            func = getattr(self._servicedesk, name)

        if func:
            return _str_vars_to_data(func)
        raise AttributeError("Non-existing keyword " + name)