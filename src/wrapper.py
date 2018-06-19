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

import requests

RE_VARS = re.compile(r"/{.*")
RE_VAR = re.compile(r"{([\w_]+?)}")


class Session:

    def __init__(self, root):
        """
        Creates the pre-emptive interface from intropestive API root.
        """

        self._is_dummy = not root.startswith("https://")
        if self._is_dummy:
            definition = open(root).read()
            definition = json.loads(definition)
            self.root = "dummy://"
        else:
            response = requests.get(root)
            self.root = root
            definition = response.json()

        self._definition = definition
        self._init()
        self.requests = requests.Session()

    def authenticate(self, username, password):
        """
        """
        self.user = self.post_authenticate(data="", auth=(username, password))
        self.requests.headers["x-auth-token"] = self.user["IdToken"]
        return self.user

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
                return self._exec("{ep_type}", "{ep_url}", locals(), **kwargs)

        '''.format(**locals()))
        exec(funct_text, {}, space)
        space["method"].__doc__ = "{endpoint}:\n{description}".format(**locals())
        setattr(self, method_name, types.MethodType(space["method"], self))

    def _exec(self, method, endpoint, args, **kwargs):
        """
        Executes the query if working with a real url
        """
        url = self.root + endpoint.format(**args).lstrip("/")
        data = args.get("data")
        request = requests.Request(method, url, data=data, params=kwargs)

        if self._is_dummy:
            return request

        request = self.requests.prepare_request(request)
        response = self.requests.send(request)
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
