#!/usr/bin/python
# -*- coding: utf-8 -*-

# Simple detector of ARP poisoning attack
# Author: Oros
# Date created : 2015/04/22

# apt-get install python-scapy
# http://secdev.org/projects/scapy/doc/usage.html
from scapy.all import sniff
from scapy.all import ARP
import commands
from gi.repository import Notify
from time import gmtime, strftime

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
				if Notify.init ("Hello world"):
					alert=Notify.Notification.new("ARP poisoning risk!","{} want {}\nBut {} is {}\n\nTarget {} ({})".format(hwsrc, psrc, psrc, arp[psrc], hwdst, pdst),"dialog-error")
					alert.show ()

				print("{} ; {} want {} ; But {} is {} ; Target {} ({})".format(strftime("%Y/%m/%d %H:%M:%S", gmtime()), hwsrc, psrc, psrc, arp[psrc], hwdst, pdst))
		else:
			arp[psrc]=hwsrc
print("Init ARP :")
for a in commands.getoutput("/usr/sbin/arp -n | tail -n +2").split("\n"):
	b=a.split()
	arp[b[0]]=b[2]
	print("{} = {}".format(b[0], b[2]))
print("Log :")
sniff(prn=check_attack,filter="arp", store=0)