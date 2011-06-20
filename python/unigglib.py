# [EN] / unigglib - Universal Gadu-Gadu IM library / 
#    * Distributed under GPL license *
# Author: Christopher 'hun7er' Marciniak (http://www.hun7er.pl/)
# GG IM protocol reference: http://toxygen.net/libgadu/protocol/ (pl)
#
# [PL] / unigglib - uniwersalna biblioteka komunikatora Gadu-Gadu dla jezyka Python /
#        * Biblioteka rozpowszechaniana na licencji GPL *
# Autor: Krzysztof 'hun7er' Marciniak (http://www.hun7er.pl/)
# Dokumentacja protokolu: http://toxygen.net/libgadu/protocol/ (pl)
#
# unigglib.py - main unigglib library module (glowny modul biblioteki)

"""
Usage example:

[code]
    from PythonGG import *

    mygg = GG(33333333, 'password')
    mygg.connect()
    mygg.login()
    mygg.disconnect()
[/code]

"""

import httplib 
import string   # i.e. split()
from socket import *
import struct
from Queue import *
from login import *
from status import *
from time import *
from packet import toHex
from messaging import *
from constants import *
from threads import *
# import threading

__author__="hun7er"
__date__ ="$2011-06-13 22:21:27$"

"""
    * to-do: *
        zsynchronizowac watki z metodami klasy GG
        zeby nadazalo sprawdzac np. potwierdzenie
        wyslania wiadomosci
        
        ...no i jakis kanal komunikacji z watkami
           jak by dalo rade.
"""

class GG:
    _uin = 666
    _pass = ''
    port = seed = 0
    ipaddr = ''
    lastMsg = ggMsg()
    s = socket(AF_INET,SOCK_STREAM)
    verboseMode = False
    listener = watchdog = 0
    locked = True
    messages = Queue()
    
    def getServerInfo(self):
        conn = httplib.HTTPConnection("appmsg.gadu-gadu.pl")
        conn.request("GET", "/appsvc/appmsg.asp?fmnumber="+str(self._uin)+"&version=&fmt=0&lastmsg=0") # get server info
        r1 = conn.getresponse()    # get response
        data = r1.read()           # sth like 0 0 91.214.237.10:8074 91.214.237.10 
        # print data # debug
        tab = data.split(' ')      # ['0', '0', '91.214.237.10:8074', '91.214.237.10'] 
        # if (self.verboseMode):
            # print "[-] Serwer: "+tab
        server = tab[3].split(':') # '91.214.237.10:8074' -> '91.214.237.10','8074'
        return server
    
    def connect(self, _ip = 0, _port = 0): # connect to the server        
        while 1:
            serverData = self.getServerInfo()
            # if _ip == 0: self.ipaddr = gethostbyname(serverData[0])
            if _ip == 0: self.ipaddr = serverData[0]
            if _port == 0: self.port = int(serverData[1])
            print "[D] Server addr: "+serverData[0]
            print "[D] Server port: "+serverData[1]
            
            try:
                self.s.connect((self.ipaddr,self.port))       # to-do: sprawdzanie czy polaczylo, jak nie to polaczyc na 443
            except error, (val, msg):                         # when socket raises the exception, msg will contain error message
                print "[!] Socket error: "+str(msg)           # print error message
                print "[E] Exception caught in GG::connect()" # some debug info
                print "[!] Reconnecting..."                   # reconnect
                # watchdog.connected = False
                # exit()                                  # we cannot continue with the error
            else:
                print '[+] Connection successfull'
                # watchdog.connected = True
                break
            
        return 0
        
    def login(self): # login
        if (self.verboseMode): 
            # print '[+] Lock acquired'
            print '[-] Logging in...'
        """if (self.locked == True):
            lockstate = 'locked'
        else:
            lockstate = 'unlocked'
        print "[D] Lock state: "+lockstate"""
        self.listener = Listener(self)
        self.listener.start()
        # data = self.s.recv(14)
        # print "Seed packet: "+toHex(data)  # debug
        # self.seed = struct.unpack("<III", data)[2]
        # print "type: "+str(struct.unpack("<III", data)[0])+"\nlength: "+str(struct.unpack("<III", data)[1])
        # for i in range(4): _seed += data[i+8]
        # print "Seed:       "+toHex(str(self.seed)) # debug
        # print "Server response: "+toHex(data)
        # print "Seed:       "+str(self.seed)
        # local = "127.0.0.1"
        # print "haslo:      "+self._pass
        while 1:
            if (self.locked == False):
                break
        hash = ggSHAHash(self._pass, self.seed)
        # print "hash hasla: "+toHex(hash)
        # print "dlugosc:    "+str(len(hash))

        loginPacket = ggLoginPkt(self._uin, hash)
        data = loginPacket.packet()
        
        print "[D] Login packet: "+toHex(data)  # debug
        print "[D] Packet len:   "+str(len(data))
        self.s.send(data)
        
        
        # data = self.s.recv(12)
        # loginState = struct.unpack("<III", data)[0]
        self.locked = True
        while 1:
            if (self.locked == False):
                break
        if (self.verboseMode):
            if self.loginState == GG_LOGIN_OK:
                print "[+] Logged in!"
            elif self.loginState == GG_LOGIN_FAILED:
                print "[!] Login error!"
            else:
                print "[?] Unknown server response; quitting..."
                exit(0)
        # self.locked = True
        self.getContactList()
        """while 1:
            if (self.locked == False):
                break"""
        # sleep(1)
        # data = struct.pack('<II', GG_LIST_EMPTY, 0)
        # if (self.verboseMode):
            # print "[D] Empty list: "+toHex(data)
        # self.s.send(data)
        # data = struct.pack('<I', GG_PING)
        # self.s.send(data)
        # data = self.s.recv(32)
        # print data
        #data = struct.pack('<I', GG_PING)
        #self.s.send(data)
        #data = struct.pack('<I', GG_PONG)
        #self.s.send(data)
        
        # listener = Listener(self.s)
        # listener.start()
        
        return self.loginState
            
        # resp = struct.unpack("<III", data)
        # print "Type: "+str(resp[0])+"\nLength: "+str(resp[1])
        # print "Server response: "+toHex(data)
        
    def getContactList (self, contacts = 0):
        if (contacts == 0):
            pack = EmptyPacket(GG_LIST_EMPTY)
            self.s.send(pack.pack())
        
    # def updateContactList
        
    def status(self, _status, _descr = ''):
        statusPkt = ggNewStatusPkt(_status, _descr)
        data = statusPkt.packet()
        print "[D] Status packet len: "+str(len(data))
        try:
            self.s.send(data)
        except error, (val, msg):
            print "[!] Error: "+msg+" ("+str(val)+")"
            print "[E] Exception caught in GG::status()" # some debug info
        else:
            if (self.verboseMode):
                print "[D] Packet: "+str(data)
                print "[D] Hex:    "+toHex(data)
                print "[+] Status changed to: 0x000"+str(_status)
        # data = self.s.recv(32)
        # print "[D] Data: "+data
        
    def msg (self, _rcpt, _msg):
        try:
            msgPkt = ggMsgPkt(int(_rcpt), _msg)
        except (AttributeError, TypeError), (val, msg):
            print "[!] Error msg: "+msg+", exception raised in GG::msg(self, _rcpt, _msg)"
            print "    Example of usage: msg(333, 'test')"
        else:
            data = msgPkt.packet()
            self.s.send(data)
            if (self.verboseMode):
                print "[D] Packet: "+str(data)
                print "[D] Hex:    "+toHex(data)
            self.locked = True
            while 1:                                
                if (self.locked == False): break       # to-do:
                                                       # dodac komunikacje z watkiem przez Queue (potwierdzenie wiad., 0x0005)
            # print "[+] Message sent to: "+str(_rcpt)
        # data = self.s.recv(32)
        # response = struct.unpack("<III", data)
        # print "[D] Resp: "+toHex(data)
        # print "[D] "+response
        
    def disconnect(self):
        self.locked = True
        self.listener.disconnect()
        while 1:
            if (self.locked == False):
                break
        self.s.close()
        if (self.verboseMode):
            print '[+] Disconnected successfully!'
    
    def __init__ (self, number, passwd, _verbose = False):
        self._uin = number
        self._pass = passwd
        # print self.ipaddr
        self.verboseMode = _verbose