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
# packet.py - GG packets (pakiety)

__author__="hun7er"
__date__ ="$2011-06-14 22:35:21$"

import struct
# from status import *
from constants import *
import time
import re

def toHex(x):
    str = "".join([hex(ord(c))[2:].zfill(2) for c in x])
    string = ''
    for i in range(len(str)):
        string += str[i]
        if (i % 2 != 0): string += ' '
    return string.upper()

def stripTags(value):
    return re.sub(r'<[^>]*?>', '', value) 

class ggPktHeader: # Gadu-Gadu Packet Header
    type = 0
    length = 0
    def packet(self):
        return struct.pack('<II', self.type, self.length)
    def __init__(self, _type, _length):
        self.type = _type
        self.length = _length
        
class EmptyPacket:
    header = 0
    def __init__ (self, _header):
        self.header = _header
    def pack (self):
        data = struct.pack('<II', self.header, 0)
        return data