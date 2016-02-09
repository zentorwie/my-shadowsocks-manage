#!/usr/bin/env python
import sslib
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json
import ssmail



def TurnOn(usrd):
	ssmail.SendMail(usrd,ssmail.TurnOnMsg(usrd))

def TurnOff(usrd):
	ssmail.SendMail(usrd,ssmail.TurnOffMsg(usrd))



def Check():
	sslib.Inhistory('Routine check')
	usrlist=sslib.GetUsrList()
	nowdate=sslib.nowdate()
	for usrname in usrlist:
		usr = sslib.MyUsr(usrlist[usrname])
		Result = usr.check()
		if Result == 'turnon':
			Inhistory('Turn on '+usrname +'\'s service')
			TurnOn(usrlist[usrname])
		if Result =='turnoff':
			Inhistory('Turn off '+usrname +'\'s service')
			TurnOff(usrlist[usrname])
		
	sslib.Inhistory('End check')


# usrlist=sslib.GetUsrList()
# usr = usrlist['acer']
# TurnOff(usr)
def Start():
	sslib.Inhistory('Command: '+'Start')
	try:
		piddir=ssetc['piddir']
	except:
		piddir='/tmp'
	pidpos=os.path.join(piddir,'ssrun.pid')
	try:		
		pid = os.fork()
		if pid:
			return
		f=open(pidpos,'a')
		# print type(os.getpid())
		f.write(str(os.getpid())+'\n')
		f.close()
		os.setsid()
	except:
		sslib.Error(2,'Run Failed')
		return
	sslib.Inhistory('Start Run')
	while 1:
		Check()
		ssetc=sslib.GetEtc()	
		try:
			sleep=ssetc['sleep']
		except:
			sleep=3600
		time.sleep(sleep)


def Stop():
	sslib.Inhistory('Command: '+'Stop')
	try:
		piddir=ssetc['piddir']
	except:
		piddir='/tmp'
	pidpos=os.path.join(piddir,'ssrun.pid')
	try:	
		f=open(pidpos,'r')
		txt=f.read().split('\n')
		f.close()
		for i in txt:
			if len(i) >0:
				# print i
				(status, output) = commands.getstatusoutput('kill '+i)
				# print output
		
		os.remove(pidpos)
		sslib.Success('Stop')
	except:
		sslib.Error(2,'Cannot Stop')