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
# constants.py - protocol constants (stale protokolu)

__author__="hun7er"
__date__ ="$2011-06-15 16:44:35$"

# status consts
NotAvailable = 0x0001
NotAvailableDescr = 0x0015
Available = 0x0002
AvailableDescr = 0x0004
Busy = 0x0003
BusyDescr = 0x0005
Invisible = 0x0014
InvisibleDescr = 0x0016
# welcome packet - sent with seed
GG_WELCOME = 0x0001
# ping <-> pong
GG_PING = 0x0008
GG_PONG = 0x0007
# contacts list
GG_LIST_EMPTY = 0x0012
GG_NOTIFY_REPLY80 = 0x0037
GG_ADD_NOTIFY = 0x000d
GG_REMOVE_NOTIFY = 0x000e
GG_STATUS80 = 0x0036
GG_USER_DATA = 0x0044
GG_FONT_BOLD = 0x01
GG_FONT_ITALIC = 0x02
GG_FONT_UNDERLINE = 0x04
GG_FONT_COLOR = 0x08
GG_FONT_IMAGE = 0x80
# packet flag for logging in
GG_LOGIN = 0x0031
# login result
GG_LOGIN_OK = 0x0035
GG_LOGIN_FAILED = 0x0043
# packet flag for sending a message
GG_SEND_MSG = 0x002d
GG_RECV_MSG80 = 0x002e
# GG_STATUS80 = GG_NOTIFY_REPLY80 = 0x05;
# GG_RECV80 = 0x02
# classes
GG_CLASS_QUEUED = 0x0001
GG_CLASS_MSG = 0x0004     # unused
GG_CLASS_CHAT = 0x0008
GG_CLASS_CTCP = 0x0010    # unused
GG_CLASS_ACK = 0x0020
# new status
GG_NEW_STATUS = 0x0038
# message flags
GG_FLAG_AUDIO = 0x00000001 # Hey man, look at me rockin' out! I'm on the radiooooooo...
GG_FLAG_VIDEO = 0x00000002 # Hey man, look at me rockin' out! I'm on the videooooooo...
GG_FLAG_MOBILE = 0x00100000
GG_FLAG_ANON_LINKS = 0x00800000
# message receival acknowledgement
GG_SEND_MSG_ACK = 0x0005
# message status (sent with ack)
GG_ACK_BLOCKED = 0x0001
GG_ACK_DELIVERED = 0x0002
GG_ACK_QUEUED = 0x0003
GG_ACK_MBOXFULL = 0x0004
GG_ACK_NOT_DELIVERED = 0x0006