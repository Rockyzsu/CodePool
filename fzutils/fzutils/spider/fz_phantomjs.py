# coding:utf-8

'''
@author = super_fazai
@File    : my_phantomjs.py
@Time    : 2017/3/21 15:30
@connect : superonesfazai@gmail.com
'''

import better_exceptions
better_exceptions.hook()

import sys
sys.path.append('..')

from scrapy.selector import Selector
import re
from gc import collect

from ..ip_pools import (
    ip_proxy_pool,
    fz_ip_pool,
    tri_ip_pool,
    get_random_proxy_ip_from_ip_pool,
)
from ..internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,
    driver_cookies_list_2_str,
)
from ..common_utils import (
    _print,
)
from ..linux_utils import get_system_type
from .selenium_always import *

# from fzutils.ip_pools import (
#     MyIpPools,
#     IpPools,
#     ip_proxy_pool,
#     fz_ip_pool,
#     tri_ip_pool,
#     get_random_proxy_ip_from_ip_pool,)
# from fzutils.internet_utils import (
#     get_random_pc_ua,
#     get_random_phone_ua,
# )
# from fzutils.common_utils import (
#     _print,
#     delete_list_null_str,
# )
# from fzutils.spider.selenium_always import *

__all__ = [
    'MyPhantomjs',
    'BaseDriver',
]

PHANTOMJS_DRIVER_PATH = '/Users/afa/myFiles/tools/phantomjs-2.1.1-macosx/bin/phantomjs'
CHROME_DRIVER_PATH = '/Users/afa/myFiles/tools/chromedriver'
FIREFOX_DRIVER_PATH = '/Users/afa/myFiles/tools/geckodriver'

# phantomjs驱动地址
EXECUTABLE_PATH = PHANTOMJS_DRIVER_PATH

# 启动类型
CHROME = 0
PHANTOMJS = 1
FIREFOX = 2

# user-agent类型
PC = 0
PHONE = 1

class MyPhantomjs(object):
    def __init__(self,
                 type=PHANTOMJS,
                 load_images=False,
                 executable_path=PHANTOMJS_DRIVER_PATH,
                 logger=None,
                 high_conceal=True,
                 headless=False,
                 driver_use_proxy=True,
                 user_agent_type=PC,
                 driver_obj=None,
                 ip_pool_type=ip_proxy_pool,
                 extension_path=None,
                 driver_cookies=None,
                 chrome_enable_automation=False,):
        '''
        初始化
        :param load_images: 是否加载图片
        :param high_conceal: ip是否高匿
        :param headless: 是否为无头浏览器(针对chrome, firefox)
        :param driver_use_proxy: chrome是否使用代理
        :param user_agent_type: user-agent类型
        :param driver_obj: webdriver对象
        :param ip_pool_type: ip_pool type
        :param extension_path: 扩展插件路径
        :param chrome_enable_automation: 是否enable-automation
        '''
        super(MyPhantomjs, self).__init__()
        self.type = type
        self.high_conceal = high_conceal
        self.executable_path = executable_path
        self.load_images = load_images
        self.headless = headless
        self.driver_use_proxy = driver_use_proxy
        self.lg = logger
        self.user_agent_type = user_agent_type
        self.ip_pool_type = ip_pool_type
        self.extension_path = extension_path
        self._cookies = driver_cookies
        self.chrome_enable_automation = chrome_enable_automation
        if driver_obj is None:
            self._set_driver()
        else:
            self.driver = driver_obj

    def _set_driver(self, num_retries=4):
        '''
        初始化self.driver，并且出错重试
        :param num_retries: 重试次数
        :return:
        '''
        try:
            if self.type == PHANTOMJS:
                self._init_phantomjs()
            elif self.type == CHROME:
                self._init_chrome()
            elif self.type == FIREFOX:
                self._init_firefox()
            else:
                raise ValueError('type赋值异常!请检查!')
            # 无法执行
            # self.bypass_spiders_derection()
        except Exception as e:
            if num_retries > 0:
                return self._set_driver(num_retries=num_retries-1)
            else:
                _print(msg='初始化driver时出错:', logger=self.lg, log_level=2, exception=e)
                raise e

    def _init_phantomjs(self):
        """
        初始化带cookie的驱动，之所以用phantomjs是因为其加载速度很快(快过chrome驱动太多)
        """
        _print(msg='init phantomjs ...', logger=self.lg)
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000  # 1秒
        cap['phantomjs.page.settings.loadImages'] = self.load_images
        cap['phantomjs.page.settings.disk-cache'] = True
        cap['phantomjs.page.settings.userAgent'] = get_random_pc_ua() if self.user_agent_type == PC else get_random_phone_ua()
        if self._cookies is not None:
            if self._cookies != '':
                cap['phantomjs.page.customHeaders.Cookie'] = self._cookies

        self.driver = webdriver.PhantomJS(executable_path=self.executable_path, desired_capabilities=cap)

        wait = ui.WebDriverWait(self.driver, 20)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        _print(msg='init over!', logger=self.lg)

        return True

    def _init_chrome(self):
        '''
        如果使用chrome请设置page_timeout=30(可用)
        :return:
        '''
        _print(msg='init chromedriver...', logger=self.lg)
        chrome_options = webdriver.ChromeOptions()
        # 设置headless
        if self.headless:
            chrome_options.add_argument('--headless')     # 注意: 设置headless无法访问网页

        chrome_options.add_argument('--disable-gpu')    # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
        # chrome_options.add_argument('window-size=1200x600')   # 设置窗口大小

        # 设置无图模式
        chrome_options.add_argument('blink-settings=imagesEnabled={0}'.format('true' if self.load_images else 'false'))

        '''无法打开https解决方案'''
        # 配置忽略ssl错误
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True

        # 设置插件
        if self.extension_path is not None:
            chrome_options.add_argument(self.extension_path)
            # 修改chrome设置相关, 开个窗口访问: chrome://settings/content, 像操作普通网页一样，进行设置，保存即可
            # 查看chromedriver版本: chrome://version/
            # 操作扩展程序(可以看到所有扩展程序id): chrome://extensions/
            # eg:
            # 播放m3u8
            # chrome-extension://emnphkkblegpebimobpbekeedfgemhof/player.html#目标.m3u8
            # chrono下载管理器
            # chrome-extension://mciiogijehkdemklbdcbfkefimifhecn/ui/index.htm

        # 设置代理
        if self.driver_use_proxy:
            proxy_ip = get_random_proxy_ip_from_ip_pool(
                ip_pool_type=self.ip_pool_type,
                high_conceal=self.high_conceal,)
            assert proxy_ip != '', '给chrome设置代理失败, 异常抛出!'
            chrome_options.add_argument('--proxy-server=http://{0}'.format(proxy_ip))

        # 修改user-agent
        chrome_options.add_argument('--user-agent={0}'.format(get_random_pc_ua() if self.user_agent_type == PC else get_random_phone_ua()))

        # 忽视证书错误
        chrome_options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])
        if self.chrome_enable_automation:
            # eg: 处理知乎登录不弹验证码
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        else:
            pass
        chrome_options.add_argument('--allow-running-insecure-content')

        self.driver = webdriver.Chrome(
            executable_path=self.executable_path,
            chrome_options=chrome_options,
            desired_capabilities=capabilities
        )
        wait = ui.WebDriverWait(self.driver, 30)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        _print(msg='init over!', logger=self.lg)

        """报错处理"""
        # linux
        # 报错处理: selenium.common.exceptions.WebDriverException: Message: Service /root/myFiles/linux_drivers/chromedriver unexpectedly exited. Status code was: 127
        # 尝试运行chromedriver
        # $ ./chromedriver
        # 报错: ./chromedriver: error while loading shared libraries: libgconf-2.so.4: cannot open shared object file: No such file or directory
        # method1(推荐):
        # 解决:
        # apt-get install chromium-browser && apt-get install libnss3 libgconf-2-4

        return True

    def _init_firefox(self):
        '''
        firefox初始化
        :return:
        '''
        _print(msg='init firefox...', logger=self.lg)
        options = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile()

        # 设置headless
        if self.headless:
            options.add_argument('--headless')

        # 设置无图模式
        if not self.load_images:
            profile.set_preference('permissions.default.stylesheet', 2)
            profile.set_preference('permissions.default.image', 2)
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        # 设置扩展插件
        if self.extension_path is not None:
            profile.add_extension(extension=self.extension_path)                   # 加载插件
            profile.set_preference('extensions.firebug.allPagesActivation', 'on')   # 激活插件

        # 设置代理
        if self.driver_use_proxy:                                                   # 可以firefox通过about:config查看是否正确设置
            proxy_ip = get_random_proxy_ip_from_ip_pool(
                ip_pool_type=self.ip_pool_type,
                high_conceal=self.high_conceal,)
            assert proxy_ip != '', '给firefox设置代理失败, 异常抛出!'
            ip = proxy_ip.split(':')[0]
            port = proxy_ip.split(':')[1]
            profile.set_preference("network.proxy.type", 1)                         # 默认是0, 1表示手工配置
            profile.set_preference("network.proxy.http", ip)
            profile.set_preference("network.proxy.http_port", port)
            profile.set_preference('network.proxy.ssl', ip)
            profile.set_preference('network.proxy.ssl_port', port)
            profile.set_preference('network.proxy.socks', ip)
            profile.set_preference('network.proxy.socks_port', port)
            profile.set_preference('network.proxy.ftp', ip)
            profile.set_preference('network.proxy.ftp_port', port)

        # 设置user-agent
        profile.set_preference("general.useragent.override", get_random_pc_ua() if self.user_agent_type == PC else get_random_phone_ua())

        # 处理异常: selenium.common.exceptions.SessionNotCreatedException: Message: Expected browser binary location, but unable to find binary in default location, no 'moz:firefoxOptions.binary' capability provided, and no binary flag set on the command line
        # 需要先安装firefox(默认安装最新版本)
        # $ sudo apt-get install firefox
        # 并且不能以root身份运行, 要以普通身份(eg: 远程调用接口)
        firefox_binary = None \
            if get_system_type() == 'Darwin' \
            else FirefoxBinary('/usr/bin/firefox')

        self.driver = webdriver.Firefox(
            firefox_binary=firefox_binary,
            executable_path=self.executable_path,
            firefox_options=options,
            firefox_profile=profile,)
        ui.WebDriverWait(self.driver, 30)  # 显示等待n秒, 每过0.5检查一次页面是否加载完毕
        _print(msg='init over!', logger=self.lg)

        return True

    def bypass_spiders_derection(self) -> None:
        """
        绕过浏览器反爬检测
        :return:
        """
        # 注意: 避免反爬检测window.navigator.webdriver为true, 认为非正常浏览器
        _js1 = """
        () => {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        }
        """
        # 绕过chrome属性检测
        _js2 = """
        () => {
            window.navigator.chrome = {
                runtime: {},
            };
        }
        """
        # 绕过Permissions检测
        _js3 = """
        () => {
            const originalQuery = window.navigator.permissions.query;
            return window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        }
        """
        # 绕过Plugins长度检测
        _js4 = """
        () => {
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        }
        """
        # 绕过the languages检测
        _js5 = """
        () => {
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        }
        """
        # print(self.driver.execute_script(script='console.log(window.navigator.webdriver);'))
        # 获取日志输出
        # print(self.driver.get_log('browser'))
        self.driver.execute_script(script=_js1)
        self.driver.execute_script(script=_js2)
        self.driver.execute_script(script=_js3)
        self.driver.execute_script(script=_js4)
        self.driver.execute_script(script=_js5)

        return

    def use_phantomjs_to_get_url_body(self,
                                      url,
                                      css_selector='',
                                      exec_code='',
                                      timeout=20,
                                      change_proxy: bool=False,
                                      change_user_agent: bool=False,):
        '''
        通过phantomjs来获取url的body
        :param url:
        :param css_selector:
        :param timeout:
        :param change_proxy:
        :param change_user_agent:
        :return: 字符串类型
        '''
        self.change_proxy = change_proxy
        self.change_user_agent = change_user_agent
        self.change_driver_proxy()

        try:
            self.driver.set_page_load_timeout(timeout)
        except:
            try: self.driver.set_page_load_timeout(timeout)
            except:
                return ''

        try:
            self.driver.get(url)
            # 隐式等待和显式等待可以同时使用
            self.driver.implicitly_wait(timeout)

            if css_selector != '':
                locator = (By.CSS_SELECTOR, css_selector)
                try:
                    WebDriverWait(self.driver, timeout, 0.5).until(EC.presence_of_element_located(locator))
                except Exception as e:
                    _print(msg='遇到错误: ', logger=self.lg, log_level=2, exception=e)
                    return ''
                else:
                    _print(msg='{0}加载完毕'.format(css_selector), logger=self.lg)

            # self.driver.save_screenshot('tmp_screen.png')
            if exec_code != '':
                # 动态执行代码
                try:
                    # 执行代码前先替换掉'  '
                    _ = compile(exec_code.replace('  ', ''), '', 'exec')
                    exec(_)
                except Exception as e:
                    # self.driver.save_screenshot('tmp_screen.png')
                    # _print(exception=e, logger=self.lg)
                    _print(msg='动态执行代码时出错!', logger=self.lg, log_level=2)
                    return ''
                # self.driver.save_screenshot('tmp_screen.png')

            main_body = self._wash_html(self.driver.page_source)
            # _print(msg=str(main_body), logger=self.lg)
        except Exception as e:
            # 如果超时, 终止加载并继续后续操作
            _print(msg='-->>time out after {0} seconds when loading page'.format(timeout), logger=self.lg, log_level=2)
            _print(msg='报错如下: ', logger=self.lg, log_level=2, exception=e)
            try:
                # 终止后续js执行
                self.driver.execute_script('window.stop()')
            except Exception:
                # 内部urllib.error.URLError or WebDriverException
                pass
            _print(msg='main_body为空!', logger=self.lg, log_level=2)
            main_body = ''

        return main_body

    def get_url_body(self,
                     url,
                     css_selector='',
                     exec_code='',
                     timeout=20,
                     change_proxy: bool=False,
                     change_user_agent: bool=False,):
        '''
        重命名
        :param url:
        :param css_selector:
        :param exec_code:
        :param timeout:
        :param change_proxy:
        :param change_user_agent:
        :return:
        '''
        return self.use_phantomjs_to_get_url_body(
            url=url,
            css_selector=css_selector,
            exec_code=exec_code,
            timeout=timeout,
            change_proxy=change_proxy,
            change_user_agent=change_user_agent,)

    def change_driver_proxy(self):
        """
        动态修改代理
        :return:
        """
        if self.type == PHANTOMJS:
            # phantomjs必进行更改ip, 因为刚开始启动时, 并未设置代理
            self.change_proxy = True
            if self.change_proxy:
                try:
                    self.dynamic_handover_ip_proxy_in_phantomjs()
                except Exception:
                    try:    # 第二次尝试
                        self.dynamic_handover_ip_proxy_in_phantomjs()
                    except Exception:
                        _print(
                            msg='动态切换ip失败!',
                            logger=self.lg,
                            log_level=2,)
                        return ''
            else:
                pass

        elif self.type == FIREFOX:
            if self.change_proxy:
                try:
                    self.dynamic_handover_ip_proxy_and_user_agent_in_fifefox()
                except Exception:
                    try:
                        self.dynamic_handover_ip_proxy_and_user_agent_in_fifefox()
                    except Exception:
                        _print(
                            msg='动态切换ip失败!',
                            logger=self.lg,
                            log_level=2,)
                        return ''
            else:
                pass

        else:
            # 其他类型不动态改变代理
            pass

    def dynamic_handover_ip_proxy_in_phantomjs(self) -> bool:
        '''
        给phantomjs切换代理
        :return:
        '''
        proxy_ip = get_random_proxy_ip_from_ip_pool(
            ip_pool_type=self.ip_pool_type,
            high_conceal=self.high_conceal, )
        assert proxy_ip != '', '动态切换ip失败!'

        # 下面方法已失效
        # try:
        #     ip, port = proxy_ip.split(':')
        #     tmp_js = {
        #         'script': 'phantom.setProxy({}, {});'.format(ip, port),
        #         'args': []
        #     }
        #     self.driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
        #     self.driver.execute('executePhantomScript', tmp_js)
        # except Exception:
        #     raise AssertionError('动态切换ip失败!')

        # 改用这个
        try:
            # 利用DesiredCapabilities(代理设置)参数值
            # 重新打开一个sessionId，相当于浏览器清空缓存后，加上代理重新访问一次url
            webdriver_proxy = WebdriverProxy()
            webdriver_proxy.proxy_type = WebdriverProxyType.MANUAL
            # eg: '1.9.171.51:800'
            webdriver_proxy.http_proxy = proxy_ip
            # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
            webdriver_proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            self.driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        except Exception:
            raise AssertionError('动态切换ip失败!')

        return True

    def dynamic_handover_ip_proxy_and_user_agent_in_fifefox(self) -> bool:
        """
        firefox动态切换proxy
        :return:
        """
        proxy_ip = get_random_proxy_ip_from_ip_pool(
            ip_pool_type=self.ip_pool_type,
            high_conceal=self.high_conceal, )
        assert proxy_ip != '', '动态切换ip失败!'

        # user_agent动态修改(采用每次都变)
        user_agent = get_random_pc_ua() if self.user_agent_type == PC else get_random_phone_ua()
        if self.change_user_agent:
            pass
        else:
            pass

        try:
            # 这里的ip和port可以根据自己的情况填充，比如通过api获取的代理ip，或者从代理池中获取也可以
            ip, port = proxy_ip.split(':')
            self.driver.get("about:config")
            _js = '''
            var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
            prefs.setIntPref("network.proxy.type", 1);
            prefs.setCharPref("network.proxy.http", "{ip}");
            prefs.setIntPref("network.proxy.http_port", "{port}");
            prefs.setCharPref("network.proxy.ssl", "{ip}");
            prefs.setIntPref("network.proxy.ssl_port", "{port}");
            prefs.setCharPref("network.proxy.ftp", "{ip}");
            prefs.setIntPref("network.proxy.ftp_port", "{port}");
　　　　　　　prefs.setBoolPref("general.useragent.site_specific_overrides",true);
　　　　　　　prefs.setBoolPref("general.useragent.updates.enabled",true);
            prefs.setCharPref("general.useragent.override","{user_agent}");
            '''.format(
                ip=ip,
                port=port,
                user_agent=user_agent)
            self.driver.execute_script(_js)
            # 不需要休眠, 上方js执行很快
            # sleep(1.)
        except Exception:
            raise AssertionError('动态切换ip失败!')

        return True

    def get_url_cookies_from_phantomjs_session(self,
                                               url,
                                               css_selector='',
                                               exec_code='',
                                               timeout=20,
                                               change_proxy: bool = False,
                                               change_user_agent: bool = False,):
        """
        从session中获取cookies
        :param url:
        :param css_selector:
        :param exec_code:
        :param timeout:
        :param change_proxy:
        :param change_user_agent:
        :return: cookies 类型 str
        """
        _print(msg='正在获取cookies...请耐心等待...', logger=self.lg)
        self.use_phantomjs_to_get_url_body(
            url=url,
            css_selector=css_selector,
            exec_code=exec_code,
            timeout=timeout,
            change_proxy=change_proxy,
            change_user_agent=change_user_agent,)
        cookies_str = ''
        try:
            cookies_list = self.driver.get_cookies()
            cookies_str = driver_cookies_list_2_str(cookies_list=cookies_list)
            # _print(msg=str(cookies), logger=self.lg)
        except Exception as e:
            _print(msg='遇到错误:', logger=self.lg, exception=e, log_level=2)

        return cookies_str

    def _wash_html(self, html):
        '''
        清洗html
        :param html:
        :return:
        '''
        html = re.compile('\n|\t|  ').sub('', html)

        return html

    def _get_cookies(self) -> dict:
        '''
        得到当前页面的cookies
        :return:
        '''
        cookies_list = self.driver.get_cookies()
        res = {}
        [res.update({i.get('name', ''): i.get('value', '')}) for i in cookies_list]

        return res

    def _get_driver(self):
        '''
        得到driver对象
        :return:
        '''
        return self.driver

    def find_element(self, by=By.CSS_SELECTOR, value=None):
        """
        查找单个element
        :param by:
        :param value:
        :return:
        """
        return self.driver.find_element(by=by, value=value)

    def find_elements(self, by=By.CSS_SELECTOR, value=None):
        """
        查找elements
        :param by:
        :param value:
        :return:
        """
        return self.driver.find_elements(by=by, value=value)

    def save_screenshot(self, file_name):
        """
        屏幕截图
        :param file_name: 保存的路径 eg: '/Screenshots/foo.png'
        :return:
        """
        return self.driver.save_screenshot(filename=file_name)

    def add_cookie(self, cookies_dict):
        """
        添加某个cookie 2 driver
        :param cookies_dict: eg: {'name' : 'foo', 'value' : 'bar'}
        :return:
        """
        self.driver.add_cookie(cookies_dict=cookies_dict)

    def delete_cookie(self, name):
        """
        删除某个cookie
        :param name:
        :return:
        """
        self.driver.delete_cookie(name=name)

    def delete_all_cookies(self):
        """
        删除driver所有cookies
        :return:
        """
        self.driver.delete_all_cookies()

    def execute_script(self, script, *args):
        """
        执行js
        :param script:
        :param args:
        :return:
        """
        return self.driver.execute_script(script=script, *args)

    def execute_async_script(self, script, *args):
        """
        执行异步js
        :param script:
        :param args:
        :return:
        """
        return self.driver.execute_async_script(script=script, *args)

    def close_current_window(self):
        """
        关闭当前窗口
        :return:
        """
        self.driver.close()

    def back(self):
        """
        当前页面回退
        :return:
        """
        self.driver.back()

    def refresh(self):
        """
        当前页面刷新
        :return:
        """
        self.driver.refresh()

    def forward(self):
        """
        返回前一页
        :return:
        """
        self.driver.forward()

    @property
    def switch_to(self):
        return self.driver.switch_to

    def switch_to_window(self, window_name):
        """
        切换到某个tab window(切换到某个窗口句柄)
        :param window_name:
        :return:
        """
        self.driver.switch_to_window(window_name=window_name)

    def switch_to_active_element(self):
        """
        切换到当前的活跃元素
        :return:
        """
        return self.driver.switch_to_active_element()

    def switch_to_alert(self):
        """
        切换到alert弹窗
        :return: 一个alert对象, 后续eg: alert = driver.switch_to_alert() alert.send_keys()
        """
        return self.driver.switch_to_alert()

    def switch_to_default_content(self):
        """
        切换回默认内容(多用于iframe切换)
        :return:
        """
        return self.driver.switch_to_default_content()

    def switch_to_frame(self, frame_reference):
        """
        Deprecated use driver.switch_to.frame
        """
        return self.driver.switch_to_frame(frame_reference=frame_reference)

    @property
    def current_url(self):
        """
        获取当前的url
        :return:
        """
        return self.driver.current_url

    @property
    def page_source(self):
        """
        当前页面的html
        :return:
        """
        return self.driver.page_source

    @property
    def current_window_handle(self) -> str:
        """
        获取当前窗口句柄name
        :return:
        """
        return self.driver.current_window_handle

    @property
    def window_handles(self) -> list:
        """
        获取所有窗口句柄name list
        :return:
        """
        return self.driver.window_handles

    def __del__(self):
        try:
            self.driver.quit()
            del self.lg
        except:
            pass
        collect()

class BaseDriver(MyPhantomjs):
    '''改名'''
    pass

def test_fz_driver_obj():
    """
    TEST 测试driver对象
    :return:
    """
    driver = None
    try:
        driver = BaseDriver(
            type=FIREFOX,
            executable_path=FIREFOX_DRIVER_PATH,
            ip_pool_type=tri_ip_pool,
            headless=False,
            load_images=True,)
        url = 'https://www.baidu.com'
        driver.get_url_body(url=url)
        search_input = driver.find_element(
            by=By.CSS_SELECTOR,
            value='input#kw')
        print('search_input:{}'.format(search_input))

        search_input.send_keys('阿发')
        driver.find_element(
            by=By.CSS_SELECTOR,
            value='input#su').click()
        driver.back()

        old_window_handle = driver.current_window_handle
        print('current_window_handle:{}'.format(old_window_handle))
        print('window_handles:{}'.format(driver.window_handles))

        # TODO driver新开窗口的方法, 通过执行js来新开一个窗口
        new_tab_window_js = 'window.open("https://www.sogou.com")'
        driver.execute_async_script(script=new_tab_window_js)
        print('window_handles:{}'.format(driver.window_handles))

        for window_handle in driver.window_handles:
            # 轮询handle
            print('switch to: {}'.format(window_handle))
            driver.switch_to_window(window_name=window_handle)
            print('current_window_handle: {}'.format(driver.current_window_handle))

        sleep(10)

    except Exception as e:
        print(e)

    finally:
        try:
            del driver
        except:
            pass

# test_fz_driver_obj()
