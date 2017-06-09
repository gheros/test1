import smtplib
import email.mime.multipart
import email.mime.text
msg=email.mime.multipart.MIMEMultipart()
msg['from']='peng.gao@credittone'
msg['to']='even蚊子@测试'
msg['subject']='test'
content='''''
 你好， 
            这是一封自动发送的邮件。 
 
       测试测试
'''
txt=email.mime.text.MIMEText(content)
msg.attach(txt)
smtp=smtplib
smtp=smtplib.SMTP()
print('222')
smtp.connect('smtp.exmail.qq.com')
smtp.login('peng.gao@credittone.com','Gp888666')
print('444')
smtp.sendmail('peng.gao@credittone.com','even.chen@credittone.com',str(msg))
smtp.quit()