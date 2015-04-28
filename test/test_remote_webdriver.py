import os
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from qubell.api.testing import *


# noinspection PyShadowingNames,PyUnusedLocal
@environment({
    "chef_11": {},  # default
    "chef_12": {
        "policies": [{
                    "action": "chefrun",
                    "parameter": "version",
                    "value": "12.2.1"
        }]
    }

})
class SeleniumGridComponentTestCase(BaseComponentTestCase):
    name = "component-selenium-grid"
    apps = [{
            "name": name,
            "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name))
            }]

    def console_base(self, capability, console, remote):
        time.sleep(15)  # let node establish connection with hub
        driver = None
        try:
            driver = webdriver.Remote(
                command_executor=str(remote),
                desired_capabilities=capability)
            driver.get(console)
            assert driver.title == "Grid Console"
        finally:
            if driver:
                driver.quit()

    @instance(byApplication=name)
    @values({"endpoints.console-url": "console", "endpoints.remote-url": "remote"})
    def test_chrome(self, instance, console, remote):
        capabilities = webdriver.ChromeOptions().to_capabilities()
        # https://sites.google.com/a/chromium.org/chromedriver/help/chrome-doesn-t-start
        # Passing '--no-sandbox' flag when creating your WebDriver session.
        # Special test environments sometimes cause Chrome to crash when the sandbox is enabled.
        capabilities['chromeOptions']['args'].append('--no-sandbox')
        self.console_base(capabilities, console, remote)

    @instance(byApplication=name)
    @values({"endpoints.console-url": "console", "endpoints.remote-url": "remote"})
    def test_firefox(self, instance, console, remote):
        self.console_base(DesiredCapabilities.FIREFOX, console, remote)
