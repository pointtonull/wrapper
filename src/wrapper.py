#!/usr/bin/env python3


"""
Dynamically defined wrapper for introspective APIs.
"""

from sys import exit
from textwrap import dedent
import json
import os
import re
import types
from configparser import ConfigParser

import requests

RE_VARS = re.compile(r"/{.*")
RE_VAR = re.compile(r"{([\w_]+?)}")

class Session:

    def __init__(self, profile="default", endpoint=None, apikey=None):
        """
        Creates the pre-emptive interface from intropestive API root.

        Reads configuration defaults for <profile>.
        Endpoint can be a http[s] url or a local file.
        Apikey will use if present.
        """

        self._config = ConfigParser()
        self._config.paths = self._config.read(os.path.expanduser("~/.qi/config"))

        try:
            profile_conf = self._config[profile]
        except KeyError as key:
            read_files = ", ".join(self._config.paths)
            if profile != "default":
                raise ValueError("Profile %s not found in conf files: %s" % (key, read_files))
            profile_conf = {}

        if endpoint is None:
            try:
                endpoint = profile_conf["endpoint"]
            except KeyError:
                raise ValueError("'endpoint' not found in conf files or explicitly provided")
        self._is_dummy = not (endpoint.startswith("https://") or endpoint.startswith("http://"))

        if apikey is None:
            apikey = profile_conf.get("qi_data_api_key")

        if self._is_dummy:
            definition = open(endpoint).read()
            definition = json.loads(definition)
            self._endpoint = "dummy://"
        else:
            if not endpoint.endswith("/"):
                endpoint += "/"
            response = requests.get(endpoint)
            self._endpoint = endpoint
            definition = response.json()

        self._definition = definition
        self._init()

        self._requests = requests.Session()
        if apikey is not None:
            self._requests.headers["x-api-key"] = apikey


#    def authenticate(self, username, password):
#        """
#        """
#        self.user = self.post_authenticate(data="", auth=(username, password))
#        if "IdToken" in self.user:
#            self._requests.headers["x-auth-token"] = self.user["IdToken"]
#        else:
#            raise ValueError("'IdToken' not found in auth answer: '%s'" % self.user)
#        return self.user


    def _init(self):
        """
        Reads the code introspective API definition and creates standar
        Python/requests wrapper.
        """
        servicename = self._definition["service"]
        self.__doc__ = "%s\n%s\n\n" % (servicename, "=" * len(servicename))

        endpoints = self._definition["endpoints"]
        endpoints = [(endpoint["url"], endpoint["description"])
                     for endpoint in endpoints]

        for endpoint, description in sorted(endpoints):
            ep_type, ep_url = endpoint.split()
            ep_name = RE_VARS.sub("", ep_url).strip("/")
            if ep_name:
                ep_vars = RE_VAR.findall(endpoint)
                self.__doc__ += "%s(%s): %s\n" % (ep_name, ", ".join(ep_vars),
                                                  ep_type)
                method_name = "%s_%s" % (ep_type.lower(), ep_name)
                self._create_method(method_name, ep_vars, ep_type, ep_url,
                                    endpoint, description)

            self.__doc__ += "%s:" % endpoint
            self.__doc__ += "%s\n" % description


    def _create_method(self, method_name, ep_vars, ep_type, ep_url, endpoint,
                       description):
        """
            Through me you pass into the city of woe:
            Through me you pass into eternal pain:
            Through me among the people lost for aye.

            Justice the founder of my fabric mov'd:
            To rear me was the task of power divine,
            Supremest wisdom, and primeval love.

            Before me things create were none, save things
            Eternal, and eternal I endure.
            All hope abandon ye who enter here.
        """

        ep_vars.insert(0, "self")
        if ep_type == "POST":
            ep_vars.append("data")
        ep_vars_str = ", ".join(ep_vars)

        space = {}
        funct_text = dedent('''

            def method({ep_vars_str}, **kwargs):
                return self._exec("{ep_type}", "{ep_url}", locals())

        '''.format(**locals()))
        exec(funct_text, {}, space)
        space["method"].__doc__ = "{endpoint}:\n{description}".format(**locals())
        setattr(self, method_name, types.MethodType(space["method"], self))


    def _exec(self, method, endpoint, scope):
        """
        Executes the query if working with a real url
        """
        url = self._endpoint + endpoint.format(**scope).lstrip("/")
        data = scope.get("data")
        kwargs = scope.get("kwargs")
        auth = kwargs.pop("auth", None)

        if kwargs:
            params = {key:value  for key, value in kwargs.items()}
            request = requests.Request(method, url, data=data, auth=auth, params=params)
        else:
            request = requests.Request(method, url, data=data, auth=auth)

        if self._is_dummy:
            return request

        request = self._requests.prepare_request(request)
        response = self._requests.send(request)
        try:
            return response.json()
        except:  # noqa
            return response.text


def main():
    """
    The main function.
    """
    print("Happy hacking")
    import IPython
    IPython.embed()


if __name__ == "__main__":
    exit(main())
