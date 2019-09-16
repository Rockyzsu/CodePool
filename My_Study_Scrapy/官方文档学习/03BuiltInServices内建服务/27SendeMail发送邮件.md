## SendeMail发送邮件

### 快速样例
```python
from scrapy.mail import MailSender
#mailer=MailSender()
mailer=MailSender.from_settings(settings)
mailer.send(to=["someone@example.com"], subject="Some subject", body="Some body", cc=["another@example.com"])
```
### MailSender 类参考
#### class scrapy.mail.MailSender(smtphost=None, mailfrom=None, smtpuser=None, smtppass=None, smtpport=None)
* smtphost:smtp 主机
* mailfrom:发送者
* smtpuser:发送者
* smtppass:认证密码
* smtpport:端口
* smtptls:强制smtp starttls
* smtpssl:强制ssl 连接
#### from_settings(settings)
从设置里面构造一个对象

#### send(to,subject,body,cc=None,attachs=(),mimetype='text/plain',charset=None)
发送邮件方法，
* to:发送目标
* subject:主题
* cc:抄送
* body:主体
* attachs；附件
* mimetype:mime类型
* charset:字符集

### mail相关设置
* MAIL_FROM: 发送地址
* MAIL_HOST:发送主机
* MAIL_PORT:端口
* MAIL_USER:认证用户名
* MAIL_PASS:认证密码
* MAIL_TLS:连接使用SSL/TSL
* MAIL_SSL:强制使用ssl连接


