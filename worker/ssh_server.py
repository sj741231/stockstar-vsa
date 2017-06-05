import workflow
import console
import paramiko
import time

strComputer = '10.5.6.23'
strUser = 'root'
strPwd = 'ezg50x=RZ'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=strComputer, username=strUser, password=strPwd)

channel = client.invoke_shell()
channel.send('ls\n')
time.sleep(3)
output=channel.recv(2024)
print(output)

#Close the connection
#client.close()
#print('Connection closed.')
