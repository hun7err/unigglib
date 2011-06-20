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
# messaging.py - messaging (wiadomosci)

__author__="hun7er"
__date__ ="$2011-06-17 21:33:45$"

from packet import *
from constants import *
import struct
import time

class ggMsg:
    sender = time = localtime = cls = attr = 0
    html = ''
    plain = ''
    def set(self, _sender, _time, _cls, _html, _plain, _attr = 0):
        self.sender = _sender
        self.time = _time
        self.localtime = time.ctime(_time)
        self.cls = _cls
        self.html = _html
        self.plain = _plain
        self.attr = _attr
    def clear(self):
        self.sender = self.time = self.localtime = self.cls = self.attr = 0
        self.html = self.plain = ''
    def __init__(self):
        pass

class ggMsgPkt:         # 
    header = ggPktHeader(GG_SEND_MSG, 0)
    rcpt = 0
    timestamp = 0
    cls = 0x08
    offset_plain = 0
    offset_attr = 0
    htmltext = ''
    plaintext = ''
    attr = ''
    def packet (self):
        data = struct.pack("<IIIII%ds%ds%ds" % (len(self.htmltext), len(self.plaintext), len(self.attr)), # struct gg_send_msg80 {
                            self.rcpt,          #   int recipient;
                            self.timestamp,     #   int seq;
                            self.cls,           #   int class;
                            self.offset_plain,  #   int offset_plain;
                            self.offset_attr,   #   int offset_attributes;
                            self.htmltext,      #   char html_message[];
                            self.plaintext,     #   char plain_message[];
                            self.attr)          #   char attributes[];
                                                # };
        # print "[D] Time: "+str(self.timestamp)
        # temp = struct.pack('>I', 0x02)
        # print "[D] Fmt:  "+toHex(fmt)
        # data += fmt
        self.header.length = len(data)
        pack = self.header.packet()+data
        return pack
        
    def __init__ (self, _rcpt, _html, _class = GG_CLASS_CHAT):
        self.cls = _class
        self.rcpt = _rcpt
        # print "[D] Rcpt: "+str(self.rcpt)
        # print "[D] Msg:  "+_html
        _html = _html.replace('<', '&lt;')
        _html = _html.replace('>', '&gt;')
        self.htmltext = '<span style="color:#000000; font-family:'+"'MS Shell Dlg 2'"+'; font-size:9pt; ">'+_html+'</span>'
        self.plaintext = stripTags(_html)+'\0'
        self.offset_plain = 21+len(self.htmltext)
        self.htmltext += '\0'
        self.offset_attr = 22+len(self.htmltext)+len(self.plaintext)
        # replace()
        self.timestamp = int(time.time())
        fmt = struct.pack('>I', 0x02)[3]
        fmt += struct.pack("<II", 0x06, 0x08)
        self.attr = fmt