import os
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException

from qubell.api.testing import *
from qubell.api.tools import retry

manifest_name = "component-selenium-grid.yml"

# noinspection PyShadowingNames,PyUnusedLocal
class SeleniumGridComponentTestCase(BaseComponentTestCase):
  @classmethod
  def timeout(cls):
      return 60 

  def console_base(self, instance, capability):
    console = instance.returnValues['endpoints.console-url']
    remote = instance.returnValues['endpoints.remote-url']

    @retry(30,4,1, Exception)
    def get_driver():
      return webdriver.Remote(
        command_executor=str(remote),
        desired_capabilities=capability)

    driver = None
    try:
      driver = get_driver()
      driver.get(console)
      assert driver.title == "Grid Console"
    finally:
      try:
        driver.quit()
      except:
        pass

@applications([{
  "name": 'Linux selenium-hub',
  "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '..', manifest_name)),
  "parameters": { "input.hub-image": { "ami": "us-east-1/ami-96a818fe", "user": "centos", "type": "linux", "hw": "m3.medium", "issudo": True, "prefix": "Selenium-hub" }}
}])
class LinuxGrid(SeleniumGridComponentTestCase):
  @instance(byApplication='Linux selenium-hub')
  def test_lin_chrome(self, instance):
        capabilities = webdriver.ChromeOptions().to_capabilities()
        # https://sites.google.com/a/chromium.org/chromedriver/help/chrome-doesn-t-start
        # Passing '--no-sandbox' flag when creating your WebDriver session.
        # Special test environments sometimes cause Chrome to crash when the sandbox is enabled.
        capabilities['chromeOptions']['args'].append('--no-sandbox')
        self.console_base(instance, capabilities)

  @instance(byApplication='Linux selenium-hub')
  def test_lin_firefox(self, instance):
        self.console_base(instance, DesiredCapabilities.FIREFOX)

@applications([{
  "name": 'Windows selenium-hub',
  "file": os.path.realpath(os.path.join(os.path.dirname(__file__), '..', manifest_name )),
  "parameters": { "input.hub-image": { "ami": "us-east-1/ami-31620c54", "user": "Administrator", "type": "windows", "hw": "m3.large", "issudo": False, "prefix": "Selenium-hub" }}
}])
class WindowsGrid(SeleniumGridComponentTestCase):
  @instance(byApplication='Windows selenium-hub')
  def test_win_chrome(self, instance):
        capabilities = webdriver.ChromeOptions().to_capabilities()
        # https://sites.google.com/a/chromium.org/chromedriver/help/chrome-doesn-t-start
        # Passing '--no-sandbox' flag when creating your WebDriver session.
        # Special test environments sometimes cause Chrome to crash when the sandbox is enabled.
        capabilities['chromeOptions']['args'].append('--no-sandbox')
        self.console_base(instance, capabilities)
  
  @instance(byApplication='Windows selenium-hub')
  def test_win_firefox(self, instance):
        self.console_base(instance, DesiredCapabilities.FIREFOX)
  
  @instance(byApplication='Windows selenium-hub')
  def test_win_ie(self, instance):
        self.console_base(instance, DesiredCapabilities.INTERNETEXPLORER)
