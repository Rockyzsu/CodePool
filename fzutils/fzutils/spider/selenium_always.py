# coding:utf-8

'''
@author = super_fazai
@File    : selenium_always.py
@connect : superonesfazai@gmail.com
'''

"""
预导入selenium常用的包

使用只需: from fzutils.spider.selenium_always import *
"""

from time import sleep

from selenium import webdriver
# WebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    NoSuchFrameException,
    NoSuchWindowException,
    NoSuchAttributeException,
)
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# proxy相关
from selenium.webdriver import Proxy as WebdriverProxy
from selenium.webdriver.common.proxy import ProxyType as WebdriverProxyType

# eg: 用于验证某些内容的颜色作为测试的一部分, 比如登入按钮的颜色变化!!
# assert login_button_background_colour.hex == '#ff69b4'
from selenium.webdriver.support.color import Color as SeleniumColor

# 选择元素可能需要相当多的锅炉板代码来自动化, Selenium支持包中有一个 Select类提供
# eg:
# select_ele = driver.find_element_by_id('selectElementID')
# select_obj = SeleniumSelect(select_ele)
# select_obj.select_by_index(1)
# select_obj.select_by_value('value1')
# select_obj.select_by_visible_text('Bread')
# 检查选择了哪些选项
# Return a list[WebElement] of options that have been selected
# all_selected_options = select_obj.all_selected_options
# Return a WebElement referencing the first selection option found by walking down the DOM
# first_selected_option = select_obj.first_selected_option
from selenium.webdriver.support.select import Select as SeleniumSelect


