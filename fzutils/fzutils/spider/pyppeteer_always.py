# coding:utf-8

'''
@author = super_fazai
@File    : pyppeteer_always.py
@connect : superonesfazai@gmail.com
'''

from pyppeteer.launcher import launch as chromium_launch
from pyppeteer.browser import Browser as PyppeteerBrowser
from pyppeteer.network_manager import Request as PyppeteerRequest
from pyppeteer.network_manager import Response as PyppeteerResponse
from pyppeteer.errors import NetworkError as PyppeteerNetworkError
from pyppeteer.page import Page as PyppeteerPage
from pyppeteer.errors import PageError as PyppeteerPageError
from pyppeteer.page import ElementHandle as PyppeteerElementHandle