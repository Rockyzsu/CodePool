# coding:utf-8

'''
@author = super_fazai
@File    : chrome_extensions.py
@connect : superonesfazai@gmail.com
'''

"""
chrome 扩展
"""

import os
import shutil
from zipfile import ZipFile

__all__ = [
    'ChromeSwitchProxyExtensioner',
]

class ChromeSwitchProxyExtensioner(object):
    '''
    chrome扩展插件: 旨在动态设置代理
        用法:
            chrome_options = webdriver.ChromeOptions()
            ext = ChromeSwitchProxyExtensioner()
            chrome_options.add_argument('--load-extension={0}'.format(ext.get_extension_dir_path()))
    '''
    def __init__(self, extension_dir='./extensions', schema='http',
                 host='127.0.0.1', port='8000', username='', passwd=''):
        self.extension_dir = extension_dir
        self.ip_pools_info = {
            'schema': schema,
            'host': host,
            'port': port,
            'username': username,
            'password': passwd,
        }

    def get_extension_dir_path(self):
        '''
        本地先生成插件内容, 再返回插件路径
        :return:
        '''
        path = "{0}/{1}_{2}".format(self.extension_dir, self.ip_pools_info['host'], self.ip_pools_info['port'])
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        with open(path + '/manifest.json', 'w') as f:
            f.write(self.get_manifest_content())
        with open(path + '/background.js', 'w') as f:
            f.write(self.get_background_content())

        return os.path.abspath(path)

    def get_extension_file_path(self):
        '''
        从.zip文件中读取插件, 再返回插件路径
        :return:
        '''
        path = "{0}/{1}_{2}.zip".format(self.extension_dir, self.ip_pools_info['host'], self.ip_pools_info['port'])
        if os.path.exists(path):
            os.remove(path)

        zf = ZipFile(path, mode='w')
        zf.writestr('manifest.json', self.get_manifest_content())
        zf.writestr('background.js', self.get_background_content())
        zf.close()

        return os.path.abspath(path)

    def get_manifest_content(self):
        '''
        mainfest.json内容
        :return:
        '''
        return '''
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        '''

    def get_background_content(self):
        '''
        background.js内容(关键内容)
        :return:
        '''
        return '''
        chrome.proxy.settings.set({{
            value: {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "{schema}",
                        host: "{host}",
                        port: {port}
                    }},
                    bypassList: ["foobar.com"]
                }}
            }},
            scope: "regular"
        }}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
            function (details) {{
                return {{
                    authCredentials: {{
                        username: "{username}",
                        password: "{password}"
                    }}
                }};
            }},
            {{ urls: ["<all_urls>"] }},
            [ 'blocking' ]
        );
        '''.format(
            schema=self.ip_pools_info['schema'],
            host=self.ip_pools_info['host'],
            port=self.ip_pools_info['port'],
            username=self.ip_pools_info['username'],
            password=self.ip_pools_info['password'])
