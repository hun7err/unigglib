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
# status.py - GG status functionality module (wszystko co zwiazane ze statusem)

__author__="hun7er"
__date__ ="$2011-06-14 22:32:42$"
from packet import *
from constants import *
import struct
    
class ggNewStatusPkt:
    header = ggPktHeader(GG_NEW_STATUS, 0)
    status = 0
    flags = 0
    descr = ''
    descr_len = ''
    def packet(self):
        """
        if (len(self.descr) == 0):
            data = struct.pack('<III',          # struct gg_new_status80 {
                            self.status,        #   int status;    
                            self.flags,         #   int flags;    
                            self.descr_len)     #   int description_size;
                                                # };
        elif (self.status == GGStatus.AvailableDescr or self.status == GGStatus.BusyDescr or self.status == GGStatus.InvisibleDescr or self.status == GGStatus.NotAvailableDescr):"""
        data = struct.pack('<III%ds' % self.descr_len, # struct gg_new_status80 {
                            self.status,        #   int status;    
                            self.flags,         #   int flags;    
                            self.descr_len,     #   int description_size;
                            self.descr)         #   char description[];
                                                # };
        self.header.length = len(data)
        pack = self.header.packet()+data
        return pack
        
    def __init__(self, _status, _descr='', _flags = GG_FLAG_ANON_LINKS):
        self.status = _status
        self.desc = _descr
        self.descr_len = len(_descr)
        self.flags = _flags