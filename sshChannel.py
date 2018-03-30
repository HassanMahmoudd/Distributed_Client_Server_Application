import paramiko
import threading
import subprocess




import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target_host = '127.0.0.1'
target_port = 22
target_port = 22
pwd = ''
un = ''
ssh.connect( hostname = target_host , username = un, password = pwd )
stdin, stdout, stderr = ssh.exec_command('ls -1 /root|head -n 5')
print "STDOUT:\n%s\n\nSTDERR:\n%s\n" %( stdout.read(), stderr.read() )


# def ssh_comm(ip,usr,passwd,cmd):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    # AutoAddPolicy automatically adding the hostname and new host key
#     client.connect(ip,username=usr,password=passwd)
#     ssh_session = client.get_transport().open_session()
#     if ssh_session.active:
#         ssh_session.ex
#
# ssh_comm('localhost', 'pythonuser', 'abc123', 'ls -l mydir')


# def sshCommand(hostname, port, username, password, command):
#     sshClient = paramiko.SSHClient()                                   # create SSHClient instance
#
#     sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())    # AutoAddPolicy automatically adding the hostname and new host key
#     sshClient.load_system_host_keys()
#     sshClient.connect(hostname, port, username, password)
#     stdin, stdout, stderr = sshClient.exec_command(command)
#     print(stdout.read())

# sshCommand("", 5000, 'mahmoud', '', 'ls -l mydir')
# if __name__ == '__main__':
#     sshCommand('localhost', 5000, 'pythonuser', 'abc123', 'ls -l mydir')