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
# login.py - authentication (logowanie/uwierzytelnianie)

__author__="hun7er"
__date__ ="$2011-06-17 21:35:52$"

from constants import *
from packet import *
import hashlib
import struct

def ggSHAHash(passwd, _seed):
    sha = hashlib.sha1()
    sha.update(passwd)               # we do not hash password but compilation of password and seed
    seed = struct.pack('<I', _seed)  # we need the binary representation of seed to be added
    sha.update(seed)                 # update with the seed...
    hash = sha.digest()              # and hash
    hash += '\0'*44                  # string length has to be 64 - it's 20 so we add 44 times '\0'
    return hash

class ggLoginPkt:       # GG login packet
    header = ggPktHeader(GG_LOGIN, 0)        # #define GG_LOGIN80 0x0031 (no length now)
    uin = 0                                  # user number
    lang = 'pl'                              # language
    hash_type = 0x02                         # 0x01 - old GG hashing, 0x02 - SHA1
    hash = ''                                # password hash (with '\0')
    status = Available                       # status set after logging in
    flags = GG_FLAG_ANON_LINKS               # connection flags
    features = 0x00002367                    # IM features
    local_ip = local_port = external_ip = external_port = 0 # unused so contains 0
    image_size = 255                         # highest acceptable image size
    unknown1 = 0x64                          # unknown (???), by default 0x64 [0xff ?]
    version_len = 0x1c                       # length of the version string
    version = 'PythonGG v1.0.0.0341 (alpha)' # IM version
    descr_size = 0                           # description length
    descr = ''                               # description
    def packet (self):                       # returns binary packet ready to be sent
        data = struct.pack('<I%dsB%dsIIIIhIhBBI%dsI%ds' % (2, 64, self.version_len, self.descr_size), # struct gg_login80 {
                            self.uin,            #      int uin;
                            self.lang,           #      char language[2]; 
                            self.hash_type,      #      char hash_type;
                            self.hash,           #      char hash[64];
                            self.status,         #      int status;
                            self.flags,          #      int flags;
                            self.features,       #      int features; 
                            self.local_ip,       #      int local_ip;
                            self.local_port,     #      short local_port;
                            self.external_ip,    #      int external_ip;
                            self.external_port,  #      short external_port;
                            self.image_size,     #      char image_size;
                            self.unknown1,       #      char unknown1;
                            self.version_len,    #      int version_len;
                            self.version,        #      char version[];
                            self.descr_size,      #      int description_size;
                            self.descr)           #      char description[]; 
                                                 # };
        # print "hash length: "+str(len(self.hash))
        # print "[D] Status: 0x000"+str(self.status)
        self.header.length = len(data)
        # print "Packet length: "+str(self.header.length)
        pack = self.header.packet()+data
        # print "[D] Pkg length: "+str(len(pack))
        # print 'hash: '+toHex(struct.unpack('<IsB%dsIIIIhIhBBIsIs' % 64, data)[3])
        # print 'length: '+str(len(struct.unpack('<IsB%dsIIIIhIhBBIsIs' % 64, data)[3]))
        return pack
        # self.packet = header+data
    def __init__ (self, _uin, _hash, _status = Available, _descr=''):
        self.uin = _uin
        self.hash = _hash
        self.status = _status
        self.descr = _descr
        self.descr_size = len(self.descr)