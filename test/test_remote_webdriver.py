import os

from test_runner import BaseComponentTestCase
from qubell.api.private.testing import instance, workflow, values
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumGridComponentTestCase(BaseComponentTestCase):
    name = "component-selenium-grid"
    apps = [{
        "name": name,
        "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name))
    }]

    def console_base(self, capability, console, remote):
        try:
            driver = webdriver.Remote(
                command_executor=remote,
                desired_capabilities=capability)
            driver.get(console)
            assert driver.title == "Grid Console"
        finally:
            driver.quit()


    @instance(byApplication=name)
    @values({"endpoints.console-url": "console", "endpoints.remote-url": "remote"})
    def test_chrome(self, instance, console, remote):
        self.console_base(DesiredCapabilities.CHROME, console, remote)

    @instance(byApplication=name)
    @values({"endpoints.console-url": "console", "endpoints.remote-url": "remote"})
    def test_firefox(self, instance, console, remote):
        self.console_base(DesiredCapabilities.FIREFOX, console, remote)
