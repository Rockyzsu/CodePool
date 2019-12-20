# coding:utf-8

'''
@author = super_fazai
@File    : sms_utils.py
@connect : superonesfazai@gmail.com
'''

"""
sms utils
"""

from requests import post

from .internet_utils import (
    get_base_headers,)
from .common_utils import json_2_dict

__all__ = [
    'sms_2_somebody_by_twilio',         # 通过twilio发送短信
    'async_send_msg_2_wx',              # 异步发送内容给微信
]

def sms_2_somebody_by_twilio(account_sid,
                             auth_token,
                             to='8618698570079',
                             _from='16083058199',
                             body='Hello from Python!') -> bool:
    '''
    通过twilio发送短信
        官网: https://www.twilio.com
        添加手机号: https://www.twilio.com/console/phone-numbers/verified
    :param account_sid: sid
    :param auth_token:
    :return:
    '''
    TwilioClinet = None
    try:
        from twilio.rest import Client as TwilioClinet
    except ImportError:
        print('ImportError: 不能导入twilio包, 可能未安装!!')

    res = False
    try:
        client = TwilioClinet(account_sid, auth_token)

        message = client.messages.create(
            to="+{}".format(to),
            from_="+{}".format(_from),
            body=body)

        # print(message.sid)
        if message.sid != '':
            res = True
    except Exception as e:
        print(e)
        pass

    return res

async def async_send_msg_2_wx(sc_key, title='新消息', msg='正文!') -> bool:
    '''
    异步发送内容给微信
    :param sc_key: key
    :return:
    '''
    headers = get_base_headers()
    headers.update({
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://sc.ftqq.com/?c=code',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    })
    data = {
        'text': title,  # title
        'desp': msg,    # content
    }
    url = 'http://sc.ftqq.com/{}.send'.format(sc_key)
    with post(url=url, headers=headers, data=data) as resp:
        send_res = json_2_dict(resp.text).get('errmsg', 'success')

    if send_res == 'success':
        return True
    else:
        return False