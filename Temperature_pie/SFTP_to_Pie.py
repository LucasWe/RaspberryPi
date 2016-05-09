
#Just a little file to transport the temperature skript to the raspberry pie (192.168.0.105)
import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.0.105", username="pi", password="raspberry")
sftp = client.open_sftp()
sftp.put("C:\Users\Lucas\PycharmProjects\Temperature_pie\Temperature.py", "/home/pi/Desktop/Temperature.py")
sftp.close()
client.close()