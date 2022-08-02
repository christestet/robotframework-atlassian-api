"""

This is a very thin wrapper for confluence. You can access all of confluence's usual
methods via CONFLUENCELibrary calls in Robot Framework.

"""
# pylint: disable=no-value-for-parameter,unused-argument,useless-object-inheritance,broad-except,consider-iterating-dictionary
import ast

from atlassian import Confluence
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


class CONFLUENCEKeywords(object):
    """
    This looks tricky but it's just the Robot Framework Hybrid Library API.
    https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#hybrid-library-api
    """

    ROBOT_LIBRARY_SCOPE = "Global"
    _confluence = Confluence
    _session = None

    def get_keyword_names(self):
        """
        Generate List of keywords from confluence lib
        """
        keywords = [
            name
            for name, function in self._confluence.__dict__.items()
            if hasattr(function, "__call__")
        ]

        keywords.append("connect_to_confluence")
        keywords.remove("__init__")

        return keywords

    def connect_to_confluence(self, url=None, username=None, password=None, **kwargs):
        """
        {session}= Connect To Confluence    https://localhost:443/confluence    user   password
        Full list of arguments https://atlassian-python-api.readthedocs.io/index.html

        Use the {session} for all your keywords
        """
        self._session = Confluence(
            url=url, username=username, password=password, **kwargs)
        logger.debug("Connected to CONFLUENCE")
        return self._session

    def __getattr__(self, name):
        func = None
        if name in self._confluence.__dict__.keys():
            func = getattr(self._confluence, name)

        if func:
            return _str_vars_to_data(func)
        raise AttributeError("Non-existing keyword " + name)