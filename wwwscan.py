#!/usr/bin/python
#-*- coding:utf-8 -*-
import requests
import sys
import platform
if platform.system() == 'Linux':
	def linux_print(msg, not_found=True):
		if not_found:
			print '\033[1;32;40m'
			print msg
			print '\033[0m'
		else:
			print msg
	_print = linux_print
elif platform.system() == 'Windows':
	from ctypes import *
	windll.Kernel32.GetStdHandle.restype = c_ulong
	h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
	globals().update(h=h)
	def windows_print(msg, not_found=True):
		if not_found:
			windll.Kernel32.SetConsoleTextAttribute(h,10)
			print msg
			windll.Kernel32.SetConsoleTextAttribute(h,7)
		else:
			print msg
	_print = windows_print

if len(sys.argv) < 2:
	print 'Usage:wwwscan.py xxxx'
	sys.exit(1)
url  = sys.argv[1]
outfile = url
if ':' in outfile:
	outfile = outfile.split(':')[0]
out = open(outfile+'.html','a')
url = 'http://%s' % url
response = requests.get(url)
server = response.headers.get('Server',None) or response.headers.get('server', None) or response.headers.get('SERVER',None)
print '--------------------------------------'
print '[Server]:\t%s' % server
print '--------------------------------------'
dictinory = 'cgi.list'
if len(sys.argv)>2:
	dictinory = sys.argv[2]
paths = open(dictinory,'r')
for path in paths:
	path = path.strip()
	if not path.startswith('/'):
		path = '/' + path
	response = requests.get(url+path)
	if response.status_code != 404:
		out.write('<a href="%s%s">%s</a>&nbsp;%s<br/>\n' % (url, path, path, response.status_code, ))
		out.flush()
	_print('%d\t%s'%(response.status_code, path,), response.status_code == 404)
out.close()
paths.close()

