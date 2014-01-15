import os

from test_runner import BaseComponentTestCase
from qubell.api.private.testing import instance, workflow, values


class ComponentTestCase(BaseComponentTestCase):
    name = "name-component"
    apps = [{
        "name": name,
        "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % "selenium-grid-manifest"))
    }]
