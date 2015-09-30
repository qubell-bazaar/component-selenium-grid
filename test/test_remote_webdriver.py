import os
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from qubell.api.testing import *


# noinspection PyShadowingNames,PyUnusedLocal
@environment({
    "default": {}
})

@applications([{
  "name": 'Linux selenium-hub',
  "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name)),
  "parameters": { "input.hub-image": { "ami": "us-east-1/ami-96a818fe", "user": "centos", "type": "linux", "hw": "m3.medium", "issudo": true, "prefix": "Selenium-hub" }}
  },
  {
  "name": 'Windows selenium-hub',
  "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '../%s.yml' % name)),
  "parameters": { "input.hub-image": { "ami": "us-east-1/ami-31620c54", "user": "Administrator", "type": "windows", "hw": "m3.large", "issudo": false, "prefix": "Selenium-hub" }}
}])

class SeleniumGridComponentTestCase(BaseComponentTestCase):

  def console_base(self, instance, capability):
    console = instance.returnValues['endpoints.console-url']
    remote = instance.returnValues['endpoints.remote-url"']
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
  
  @instance(byApplication='Linux selenium-hub')
  def test_chrome(self, instance):
        capabilities = webdriver.ChromeOptions().to_capabilities()
        # https://sites.google.com/a/chromium.org/chromedriver/help/chrome-doesn-t-start
        # Passing '--no-sandbox' flag when creating your WebDriver session.
        # Special test environments sometimes cause Chrome to crash when the sandbox is enabled.
        capabilities['chromeOptions']['args'].append('--no-sandbox')
        self.console_base(instance, capabilities, console, remote)

  @instance(byApplication='Linux selenium-hub')
  def test_firefox(self, instance):
        self.console_base(DesiredCapabilities.FIREFOX, console, remote)


  @instance(byApplication='Windows selenium-hub')
  def test_chrome(self, instance):
        capabilities = webdriver.ChromeOptions().to_capabilities()
        # https://sites.google.com/a/chromium.org/chromedriver/help/chrome-doesn-t-start
        # Passing '--no-sandbox' flag when creating your WebDriver session.
        # Special test environments sometimes cause Chrome to crash when the sandbox is enabled.
        capabilities['chromeOptions']['args'].append('--no-sandbox')
        self.console_base(instance, capabilities, console, remote)
  
  
  @instance(byApplication='Windows selenium-hub')
  def test_firefox(self, instance):
        self.console_base(DesiredCapabilities.FIREFOX, console, remote)
  
  @instance(byApplication='Linux selenium-hub')
  def test_ie(self, instance):
        self.console_base(DesiredCapabilities.INTERNETEXPLORER, console, remote)
