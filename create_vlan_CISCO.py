import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
passwd = "pass"
client.connect(hostname='192.168.0.1',
               username='user',
               password='pass',
               port=22)

vlan_begin = 3000
vlan_end = 3256

with client.invoke_shell() as ssh:
	ssh.send("enable\n")
	ssh.send("{}\n".format(passwd))
	print("root")
	ssh.send("conf t\n")
	print("terminal")
	while vlan_begin <= vlan_end:
		ssh.send("interface Vlan{}\n".format(vlan_begin))
	#	print("vlan {}  create".format(vlan_begin))
	#	ssh.send("state active\n")
	#	print("{}  active".format(vlan_begin))
	#	ssh.send("ip dhcp relay information trusted\n")
		ssh.send("no ip unnumbered Loopback1\n")
		ssh.send("ip unnumbered Loopback2\n")
	#	ssh.send("ip helper-address 10.0.0.1\n")
	#	ssh.send("no ip redirects\n")
	#	ssh.send("no ip unreachables\n")
	#	ssh.send("ip local-proxy-arp\n")
	#	ssh.send("ip route-cache same-interface\n")
	#	ssh.send("hold-queue 1500 in\n")
		print("Int Vlan {}  created".format(vlan_begin))
		vlan_begin += 1
		time.sleep(3)

client.close()
