"""

This is a very thin wrapper for bitbucket. You can access all of bitbucket's usual
methods via BITBUCKETLibrary calls in Robot Framework.

"""
# pylint: disable=no-value-for-parameter,unused-argument,useless-object-inheritance,broad-except,consider-iterating-dictionary
import ast

from atlassian import Bitbucket
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


class BITBUCKETKeywords(object):
    """
    This looks tricky but it's just the Robot Framework Hybrid Library API.
    https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#hybrid-library-api
    """

    ROBOT_LIBRARY_SCOPE = "Global"
    _bitbucket = Bitbucket
    _session = None

    def get_keyword_names(self):
        """
        Generate List of keywords from bitbucket lib
        """
        keywords = [
            name
            for name, function in self._bitbucket.__dict__.items()
            if hasattr(function, "__call__")
        ]

        keywords.append("connect_to_bitbucket")
        keywords.remove("__init__")

        return keywords

    def connect_to_bitbucket(self, url=None, username=None, password=None, **kwargs):
        """
        Connect To Bitbucket    https://localhost:443/bitbucket    user   password
        Full list of arguments https://atlassian-python-api.readthedocs.io/index.html
        Use the {session} for all your keywords
        """
        self._session = Bitbucket(
            url=url, username=username, password=password, **kwargs)
        logger.debug("Connected to BITBUCKET")
        return self._session

    def __getattr__(self, name):
        func = None
        if name in self._bitbucket.__dict__.keys():
            func = getattr(self._bitbucket, name)

        if func:
            return _str_vars_to_data(func)
        raise AttributeError("Non-existing keyword " + name)