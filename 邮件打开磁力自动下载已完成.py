import imapclient,pyzmail,re,time,subprocess,smtplib
from email.mime.text import MIMEText
mailaddr = '' #发送邮件地址
smtpaddr = '' #接收邮件smtp地址
port = 465 #接收SMTP地址端口
usr = '' #接收邮件的邮箱地址
passwd = '' #接收邮件的邮箱地址密码
sender = '' #发送邮件邮箱
qBittorent = "C:\Program Files (x86)\qBittorrent\qbittorrent.exe" #BT及磁力下载的程序路径

def takemail():
    connect = imapclient.IMAPClient(mailaddr)
    try:
        connect.login(usr,passwd)
    except Exception as err:
        print('登陆失败:',err)
    bodys = []
    deletemail = []
    connect.select_folder('INBOX')
    msno = connect.search('FROM'+sender)
    maildict = connect.fetch(msno,['BODY[]'])
    for uid in maildict.keys():
        message = pyzmail.PyzMessage.factory(maildict[uid][b'BODY[]'])
        if message.text_part != None:
            body = message.text_part.get_payload().decode(message.text_part.charset)
            deletemail.append(uid)
        elif message.html_part != None:
            body = message.html_part.get_payload().decode(message.html_part.charset)
            deletemail.append(uid)
        bodys.append(body)
#    找到相应的正文后删除邮件
    if len(deletemail) > 0:
        connect.delete_messages(deletemail)
        connect.expunge()
    connect.logout()
#将正文的内容返回    
    return bodys

def downandreturn():
    #查找所有的正文内容，并先将列表中所有的字符按空格分开，存为列表b，再遍历b中所有字符，检查是否为下载类型
    detail = takemail()
    returnmessage = ''
    for i in range(len(detail)):
        b = detail[i].split('\n')
        for k in b:
            if k.startswith('magnet'):
                subprocess.Popen(qBittorent + ' ' + k)
                returnmessage += '下载magnet链接---(   '+k+'   ):已完成!\n'
    if returnmessage == '':
        print('没有收到可用的磁力链接信息！等待邮件接收可用的信息')
    else:
        msg = MIMEText(returnmessage,'plain','utf-8')
        msg['Subject'] = "下载mgent回执！"
        msg['From'] = usr
        msg['To'] = sender
        connsmtp=smtplib.SMTP_SSL(smtpaddr,port)
        connsmtp.login(usr,passwd)
        connsmtp.ehlo()
        connsmtp.sendmail(usr,sender,msg.as_string())
        connsmtp.quit()
        print('回执%s的邮件已经发送成功!\n请到%s中接收邮件!' % (sender,sender))
    
    
choice=input('请选择是否长期执行（选择否则为执行一次）Y/N:')
time_m=int(input('请选择多少分钟检查一次邮件下载磁力文件,单位（分钟）:'))
if choice.lower() == 'y':
    while True:
        downandreturn()
        time.sleep(60 * time_m)
elif choice.lower() == 'n':
    downandreturn()
else:
    print('选择错误，只接收Y或N无论大小写单个字符！请重新运行此脚本！')
    
