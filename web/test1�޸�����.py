import paramiko
def cpasswd():
    port = 22
    username = 'ubuntu'
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect('106.75.156.102', port, username, 'test12345')
    stdin, stdout, sterr = s.exec_command('echo %s | passwd --stdin root' % ('credittone'))
    print (stdout.read())
    s.close()
if __name__ == '__main__':
    cpasswd()