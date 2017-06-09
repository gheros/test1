from pexpect import pxssh
import pexpect
import getpass
s = pxssh.pxssh()
s.login('106.75.156.102','ubuntu', 'test12345')
s.sendline('ls -l')