#!/usr/bin/python
# -*- coding: utf-8 -*-

# Simple detector of ARP poisoning attack
# Author: Oros
# Date created : 2015/04/22
# Update : 2015/04/23

# apt-get install python-scapy
# http://secdev.org/projects/scapy/doc/usage.html
from scapy.all import sniff
from scapy.all import ARP
import commands
from time import gmtime, strftime

# If you didn't have "sudo", and you have got this error : "gi._glib.GError: The connection is closed"
# you can set the user name who run desktop
# Example :
# user="Bob"
user=""

if user=="":
	from gi.repository import Notify

# arp={"IP":"MAC","IP":"MAC",...}
arp={}

def check_attack(x):
	if ARP in x and x[ARP].op == 2:
		hwsrc= x.sprintf("%ARP.hwsrc%")
		psrc= x.sprintf("%ARP.psrc%")
		hwdst= x.sprintf("%ARP.hwdst%")
		pdst= x.sprintf("%ARP.pdst%")
		if psrc in arp:
			if arp[psrc]!=hwsrc:
				if bash_notif:
					commands.getoutput("su - {} -c 'notify-send \"ARP poisoning risk!\" \"{} want {}\nBut {} is {}\n\nTarget {} ({})\" --icon=dialog-error'".format(user,hwsrc, psrc, psrc, arp[psrc], hwdst, pdst))
				else:
					if Notify.init ("Hello world"):
						alert=Notify.Notification.new("ARP poisoning risk!","{} want {}\nBut {} is {}\n\nTarget {} ({})".format(hwsrc, psrc, psrc, arp[psrc], hwdst, pdst),"dialog-error")
						alert.show ()
				print("{} ; {} want {} ; But {} is {} ; Target {} ({})".format(strftime("%Y/%m/%d %H:%M:%S", gmtime()), hwsrc, psrc, psrc, arp[psrc], hwdst, pdst))
		else:
			arp[psrc]=hwsrc

try:
	if Notify.init ("Hello world"):
		alert=Notify.Notification.new("ARP poisoning detector","Start","dialog-information")
		alert.show ()
		bash_notif=False
	else:
		commands.getoutput("su - {} -c 'notify-send \"ARP poisoning detector\" \"Start\" --icon=dialog-information'".format(user))
		bash_notif=True
except:
	commands.getoutput("su - {} -c 'notify-send \"ARP poisoning detector\" \"Start\" --icon=dialog-information'".format(user))
	bash_notif=True

print("Init ARP :")
for a in commands.getoutput("/usr/sbin/arp -n | tail -n +2").split("\n"):
	b=a.split()
	arp[b[0]]=b[2]
	print("{} = {}".format(b[0], b[2]))
print("Log :")
sniff(prn=check_attack,filter="arp", store=0)