import unittest
from os import path

from .context import ROOT, HERE
from .context import wrapper

"""
{
  "service": "Example API",
  "endpoints": [
    {
      "url": "POST /auth",
      "description": "data is the complex thingy"
    },
    {
      "url": "GET /describe/{thingy}",
      "description": "Get info for given thingy"
    },
    {
      "url": "GET /",
      "description": "Self-documenting endpoint."
    }
  ]
}
"""

class DummyInterface(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.interface = wrapper.Session(path.join(HERE, "definition.json"))

    def test__is_dummy(self):
        assert self.interface._is_dummy

    def test__endpoints__present(self):
        endpoints = ["get_learn", "get_instrument", "get_drivers", "post_learn"]
        for endpoint in endpoints:
            assert endpoint in dir(self.interface), "%s not defined" % endpoint

    def test__drivers__runs(self):
        instrument = "msft"
        assert self.interface.get_drivers(instrument)
