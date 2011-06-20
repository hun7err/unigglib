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
# threads.py - threading - receiving packets and connection watchdog (watki - odbieranie i kontrola polaczenia)

__author__="hun7er"
__date__ ="$2011-06-17 23:27:22$"

from threading import Thread
from packet import toHex
from constants import *
from socket import error
import struct
# import time

class Listener (Thread):
    _socket = 0
    gg_inst = 0
    connected = True
    def run(self):
        while (self.connected == True):
            try:
                header = self._socket.recv(8)
                if (len(header) > 0):
                    info = struct.unpack('<II', header)
                    packet = self._socket.recv(info[1])
                # dane = self._socket.recv(1024)
            except error, (val, msg):
                print "[!] Error: "+msg+" ("+str(val)+")"
                print "[E] Exception caught in Listener::run()" # some debug info
                self.connected = False
                exit()
            else:
                if (len(header) > 0):
                    print "[L] Got packet!"
                    print "[L] Header: "+toHex(header)
                    print "[L] Packet: "+toHex(packet)
                    # print header
                    """
                        * to-do: *
                            odczytywac z pakietu 8 bajtow po czym rozdzielac
                            przez struct.unpack('<II', fragment) na typ i dl.
                            i wypisywac na standardowe wyjscie
                    """
                    """frag = ''
                    for i in range(8):
                        frag += dane[i]"""
                    # print "[L] frag.: "+toHex(frag)
                    # pack = struct.unpack('<II', frag)
                    # if (len(dane) == 12):
                    # print "[L] Packet type: "+toHex(pack[0])
                    # print "[L] Packet len.: "+str(pack[1])
                    if (info[0] == GG_WELCOME):
                        print "[L] Seed received"
                        self.gg_inst.seed = struct.unpack("<I", packet)[0]
                        self.gg_inst.locked = False
                    elif (info[0] == GG_LOGIN_OK):
                        self.gg_inst.loginState = GG_LOGIN_OK
                        self.gg_inst.locked = False
                    elif (info[0] == GG_LOGIN_FAILED):
                        self.gg_inst.loginState = GG_LOGIN_FAILED
                        self.gg_inst.locked = False
                    elif (info[0] == GG_RECV_MSG80):
                        msg_info = ''
                        for i in range(8):
                            msg_info += packet[16+i]
                        print "[D] Msg info: "+toHex(msg_info)
                        offset_plain = struct.unpack('<II', msg_info)[0]
                        offset_attr = struct.unpack('<II', msg_info)[1]
                        html_len = offset_plain - 25
                        plain_len = offset_attr - offset_plain - 1
                        msg_val = ''
                        for i in range(25+html_len+plain_len): # 28?
                            msg_val += packet[i]
                        print toHex(msg_val)
                        # print "[L] HTML len : "+str(html_len)
                        # print "[L] Plain len: "+str(plain_len)
                        msg = struct.unpack('<IIIIII%dsc%ds' % (html_len, plain_len), msg_val)
                        # def set(self, _sender, _time, _cls, _html, _plain, _attr = 0):
                        self.gg_inst.lastMsg.set(msg[0], msg[2], msg[3], msg[6], msg[8])
                        # print msg
                        # print "[L] Got message!"
                        # print "[L] From: "+str(msg[2])
                        # print "[L] Text: "+str(msg[10])
                        # print "[L] Time: "+time.ctime(msg[4])
      # !!!          elif (info[0] == GG_SEND_MSG_ACK):    # to-do:
                        #self.gg_inst.locked = False       # a) dodac komunikacje z glownym watkiem poprzez Queue (patrz: docs.python.org)
                        
                        
    def __init__ (self, _gg_inst):
        Thread.__init__(self)
        self._socket = _gg_inst.s
        self.gg_inst = _gg_inst
    def disconnect(self):
        self.connected = False
        self.gg_inst.locked = False
                        
                
class WatchDog (Thread):
    _socket = 0
    connected = False
    gg_inst = 0
    def check(self):
        dane = struct.pack('<I', GG_PING)
        self._socket.send(dane)
        czas = int(time())
        ponged = False
        while ( int(time())-czas < 10 ):
            dane = self._socket.recv(8)
            if (len(dane) == 4):
                packet = struct.unpack('<I', dane)
                if (packet == GG_PONG):
                    ponged = True
                    break
        if (ponged != True):
            self.connected = False
            self.gg_inst.disconnect()
            self.gg_inst.connect()
            self.gg_inst.login()
    def __init__ (self, _gg_inst):
        Thread.__init__(self)
        self._socket = _gg_inst.s
        self.gg_inst = _gg_inst
    def run (self):
        while 1:
            if (self.connected):
                t = threading.Timer(4*3600, check)
                t.start()
            else:
                t.cancel()