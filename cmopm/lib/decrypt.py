# -*- coding: utf_8 -*-

'''
Created on April 24, 2013

@author: Siye/Sye/Student
@copyright: Copyright 2013 Siye/Sye/Student - All Rights Reserved.
@summary: Holds class definitions for binary decryption
'''

from binascii import hexlify, unhexlify
import struct
import random
import ctypes
import copy
import array
import math
import datetime
import logging

# Attach logger
log = logging.getLogger(__name__)

# Dependencies
from PyQt4.QtCore import SIGNAL

class XOR32(object):
    seedY = ctypes.c_uint(362436069) # Hardcoded from source. Likely to change in future revisions.
    seedZ = ctypes.c_uint(521288629)
    seedW = ctypes.c_uint(88675123)

    def __init__(self, key):
        self.key = ctypes.c_uint(int(471283569) + int(key))

    def next(self):
        return self._rotate()

    def _rotate(self):
        ''' Internal. Cycle seed values '''
        num = ctypes.c_uint(self.key.value ^ self.key.value << 11)

        self.key = copy.copy(self.seedY)
        self.seedY = copy.copy(self.seedZ)
        self.seedZ = copy.copy(self.seedW)
        self.seedW = ctypes.c_uint(self.seedW.value ^ self.seedW.value >> 19 ^ (num.value ^ num.value >> 8))
        #print "num: ", num.value, "X: ", self.key.value, "Y: ", self.seedY.value, "Z: ", self.seedZ.value, "W: ", self.seedW.value
        return self.seedW.value

class TCP(object):
    ''' A TCP class reversed from the CMO code '''
    XOR32_seed = 0
    srvComMap = {20002: {"Command": "Load Maid", "Comment": "Maid Object Data. Default maid name is: \"Novice Maid Lv.0\""},
                21002: {"Command": "Load Maid", "Comment": "Profiles & Metadata (Miyouji?)"},
                21006: {"Command": "Load Maid", "Comment": "Jobs & Job Stats (Currently only 3)"},
                21008: {"Command": "Maid Job", "Comment": "Process Job Attempt. Success, Failure, Level Up, etc."},
                21018: {"Command": "No Action", "Comment": "Does Nothing!"},
                21020: {"Command": "No Action", "Comment": "Does Nothing!"},
                21022: {"Command": "Maid Loan", "Comment": "On success, modifies \"Maid Loans\" property."},
                21024: {"Command": "Maid Borrow/Swap", "Comment": "[Not Implemented Yet] You need \"esute\" tickets for this. Cost only 1!"},
                21026: {"Command": "Buy Item", "Comment": "Costs 1 \"esute\" ticket."},
                21028: {"Command": "Maid Borrow", "Comment": "Processes Result. Seems unused. Doesn't do anything."},
                22002: {"Command": "Use Item", "Comment": "Use an item on a maid. Item rank or class can increase here."},

                0: {"Command": "Logout Success", "Comment": "Disconnected from the server."},
                1: {"Command": "Log Server String", "Comment": "Logs the payload string and com variables to the console."},
                2: {"Command": "Log Server Error", "Comment": "Logs the error string sent as payload to console"},
                4: {"Command": "Server Heartbeat", "Comment": "Server got heartbeat."},
                5: {"Command": "Log Duplicate Login Confirmation", "Comment": "Logs to console that server sent a dup login confirmation. Odd."},

                30000: {"Command": "UserData Ready", "Comment": "Userdata server has is ready. Client requests it here."},
                30002: {"Command": "Maid Profile Props", "Comment": "Load items/props for a maid profile."},
                30004: {"Command": "Maid Profiles", "Comment": "Final UserData loading step. Process all maids you own. Notes the ones on Loan."},
                30006: {"Command": "Create Maid", "Comment": "Server response about creating a new maid. Can fail."},
                30010: {"Command": "Buy Item", "Comment": "Need \"S Points\". Can fail in many ways."},
                30012: {"Command": "Pre Buy Item", "Comment": "Before actually buying item, this will ask you first. Can fail if you want too many items."},
                30014: {"Command": "Scratch Ticket", "Comment": "Modifies item counts."},
                30016: {"Command": "Edit Fatigue", "Comment": "Adds or Resets Fatigue on all maids."},
                30018: {"Command": "Charge Item", "Comment": "Process charging and item. Can fail in many ways."},
                30020: {"Command": "Stamp Item", "Comment": "Process stamping of an item. Can fail. Not sure what stamping is."},
                30022: {"Command": "RankUp Item", "Comment": "Process ranking up an item. Can fail."},
                30026: {"Command": "Wait Payment Processing", "Comment": "Server says to wait until payment processing is done."},
                30028: {"Command": "Process Coupon", "Comment": "Process redeeming a coupon. Coupons do many things."},
                30030: {"Command": "Last Login Time", "Comment": "Server sent when you last logged in."},
                30032: {"Command": "No Action", "Comment": "Does Nothing!"},
                30034: {"Command": "Event Jump", "Comment": "Server sent results of a event jump."},
                30036: {"Command": "Process Gift | BONUS!", "Comment": "Server sent a gift (type of coupon). Called a \"Continuous Login Bonus\""},
                30038: {"Command": "Log Server Debug", "Comment": "Logs the string sent to the log."},
                30040: {"Command": "Log Alert User", "Comment": "Shows a dialog to user with msg sent by server."},
                30042: {"Command": "Item Effects", "Comment": "Server sent list of item effects. Will que these effects to show user."},
                30044: {"Command": "Update UserData", "Comment": "Server sends latest user data. Logs kisspoints(SyojiPoint) to log."},

                29998: {"Command": "Set Maid Props", "Comment": "Server sent maid prop list. Assign to the maid[0]. "},

                11002: {"Command": "Login XOR32 Seed", "Comment": "Server sent its local time and the XOR32 seed. Save these."},
                11004: {"Command": "Login Server Response", "Comment": "Server sends response of login attempt. On success, mode changes. Can fail easily."},
                11006: {"Command": "Guest Account Generation", "Comment": "Server sends the credentials for a new guest account."}
                }
    cliComMap = {11001: {"Command": "Ask for XOR32 Seed", "Comment": "Start the login process, get a XOR32 seed."},
                11003: {"Command": "Login Attempt", "Comment": "Client Login. Send Encrypted Username and Password/"},
                11005: {"Command": "Request New User ID & Pass", "Comment": "If making new user, ask for new credentials from server."},

                20001: {"Command": "Create Maid", "Comment": "I think..."},
                
                21001: {"Command": "Update Maid Property", "Comment": "Send server upddated maid variables. Name, Type(?), etc."},
                21003: {"Command": "Set Maid Birthday", "Comment": "Set Maid Birthday"},
                21005: {"Command": "Open MainMenu(?)", "Comment": "Sent during MMenu load. Tells server current maid."},
                21007: {"Command": "Attempt Maid Job", "Comment": "If enough HP, try to do a job/work."},
                21009: {"Command": "Request Server Maid Metadata", "Comment": "Asks server for the data it has on a maid. (Stamina, etc)"},
                21011: {"Command": "Start Sexy Time", "Comment": "Tell server starting sex time maid."},
                21013: {"Command": "Finish Sexy Time", "Comment": "Tell server done with sex time. Final Tally."},
                21017: {"Command": "Update Maid Sexy Value", "Comment": "Sends new \"Hyouka\" value to server about maid."},
                21021: {"Command": "Lend Maid", "Comment": "Client sends maid info on a maid being lent."},
                21023: {"Command": "Borrow Maid", "Comment": "Client asks to borrow a maid. Works?"},
                21025: {"Command": "Maid Update Rank/Title", "Comment": "Update a value of maid concerning ranking/title."},
                21027: {"Command": "Fair Maid Registration(?)", "Comment": "No idea."},

                22001: {"Command": "Register/Modify Maid", "Comment": "Add HP (1 or 999 \"EX\") to maid or Send server maid info, to register a new maid."},
                22003: {"Command": "Apply Item Request", "Comment": "Request to use an item."},

                30001: {"Command": "Request UserData", "Comment": "Client asks server for userdata."},
                30003: {"Command": "Request Maid Profiles", "Comment": "Ask for all maids I own or am borrowing."},
                30005: {"Command": "Create Default Maid Object (Kasumi)", "Comment": "Generate \"Kasum\", place at zero vector position. Kasumi is default maid object."},
                30007: {"Command": "Dismiss Maid", "Comment": "Let a maid go. :("},
                30009: {"Command": "Buy Ticket/Item (Free)", "Comment": "Buy esute or other item. May be free."},
                30011: {"Command": "Buy MaidProp/Item", "Comment": "Buy Something or \"recharge it\" if you are out."},
                30013: {"Command": "Buy Ticket/Item", "Comment": "Buy an item if it costs something."},
                30017: {"Command": "Recharge Item", "Comment": "Recharge a depleted item."},
                30019: {"Command": "Sell Item", "Comment": "Sell an item."},
                30021: {"Command": "Rank-Up Item", "Comment": "Attemp to Rank an item up."},
                30027: {"Command": "Redeem Coupon", "Comment": "Send coupon encoded and maid to redeem against."},
                30029: {"Command": "Waiting on Login Response", "Comment": "Waiting for server to get back to us concerning a login."},
                30031: {"Command": "Request Info on Item", "Comment": "Ask server for information on a owned item."},
                30033: {"Command": "Announce Event Jump(?)", "Comment": "Tell server about event jump due to an item."},
                30035: {"Command": "Request Notifications", "Comment": "Ask server for list of notifications."},
                30037: {"Command": "Leaving Video Recording" , "Comment": "Tell server ending video recording mode."},
                30043: {"Command": "Reload Item", "Comment": "Reload information on a item from server."},

                0: {"Command": "Server Disconnect", "Comment": "Tell server I am disconnecting."},
                1: {"Command": "Client Heartbeat", "Comment": "Ping server every ~120 seconds"},
                3: {"Command": "Client Ping", "Comment": "Ping Server. Used to get server latency."},                
                }

    def __init__(self, parent):
        super(TCP, self).__init__()

        self.parent = parent

    def checkPacket(self, data):
        ''' Parse packet, decode, validate checksum, emit'''

        # Parse Header (10 Bytes)
        header = list(struct.unpack('!BHHIB', unhexlify(data[:20])))

        # Start Crypto
        aXOR32 = XOR32(33 + self.XOR32_seed + header[1])

        # Alter Vars Against Crypto
        header[0] ^= self.getByteAsInt(aXOR32.next())
        header[2] ^= self.getShortAsInt(aXOR32.next())
        header[3] ^= aXOR32.next()
        header[4] ^= self.getByteAsInt(aXOR32.next())

        # Compute TMP Checksum
        checksumTmp = ctypes.c_ushort(header[2] + header[3] + (header[3] >> 16) + header[4] + header[0])

        if header[0] == 255:
            log.debug("Resetting comBufferSize to %d." % int(header[3]))
            header[0] = int(header[3])

        # Process Payload
        payloadDec = array.array('B')
        if len(data) > 20:
            data = unhexlify(data[20:])
            if header[0] > 1384:
                log.debug("Header longer then possible data! Abort Processing!")
            else:
                if len(data) != header[0]:
                    log.debug("Payload Length MisMatch! Data is %d bytes. Header says %d bytes." % (len(data), header[0]))
                    if len(data) < header[0]:
                        log.debug("Less actual data than what header wants. 0 Padding.")
                        diff = header[0] - len(data)
                        data = data + ('\x00' * diff)
                    else:
                        log.debug("More actual data than header expects, trimming")
                        data = data[:header[0]]

                payload = list(struct.unpack('!%dB' % header[0], data))
                for byte in payload:
                    #print "Byte: ", byte
                    byte ^= self.getByteAsInt(aXOR32.next())
                    #print "Byte Dec: ", byte
                    payloadDec.append(byte)
                    # Process Checksum
                    checksumTmp.value += ctypes.c_ushort(byte).value

                # Processing Done
                #print "Header Post:", header
                #print "CheckSumTmp:", checksumTmp.value
                #print "Payload:", payloadDec
                #print "Final Checksums:", checksumTmp.value, header[1]

        # Test Checksums
        if checksumTmp.value == header[1]:
            self.processCommand(header[2], header[3], header[4], payloadDec)
        else:
            log.debug("Checksum Mis-match: %s %s!" % (checksumTmp.value, header[1]))

    def processCommand(self, com1, com2, com3, payload):
        ''' Given Packet Variables process the command received '''

        # Store XOR32 Seed
        if int(com1) == 11002:
            self.XOR32_seed = com2 - 768345
            self.parent.emit(SIGNAL("changeXOR32SEED"), self.XOR32_seed)

        outbound = self.parent.outbound
        try: 
            if outbound:
                desc = self.cliComMap[com1]
            else:
                desc = self.srvComMap[com1]
        except KeyError:
            desc = {"Command": "Unknown!", "Comment": "No entry in lookup table for this packet. Never seen before!"}

        decoded = self.decodePacketLogic(int(com1), int(com2), int(com3), payload)

        #payload_format = "[%s][%s][Com1: %d][Com2: %d][Com3: %d][Payload (%d bytes): %s]" % (desc["Command"], desc["Comment"], com1, com2, com3, len(payload), hexlify(payload.tostring()))
        self.parent.emit(SIGNAL("PacketMsg"), desc["Command"], desc["Comment"], decoded, com1, com2, com3, len(payload), hexlify(payload.tostring()), outbound, self.parent.countPacketsCaptured)

    def decodePacketLogic(self, com1, com2, com3, payload):
        ''' Given arguments, attempt to see what is actually being done '''

        res = ""
        if com1 == 11001:
            res += "Tell server I want to connect. All other data is random bytes. "
        elif com1 == 11002:
            res += "XOR32 Seed is %d. " % (com2 - 768345)
            sVer = self.getInt32(payload)
            res += "Server Version: %s. " % sVer
            if sVer is not 0:
                res += "Client Version is Different from Server! "
            else:
                sEpoch = self.getInt32(payload[:-4])
                res += "Connection Start: %s. " % datetime.datetime.fromtimestamp(sEpoch).strftime('%Y-%m-%d %H:%M:%S')
        elif com1 == 11003:
            uNameLen = self.getInt32(payload[-1])
            res += "Login with username: %s. Password is RSA encrypted. " % self.getString(payload[:-5])
        else:
            res += "No Comment"
        return res

    def getString(self, data, count):
        ''' Given data and a character count, return a string '''

        return str(bin(data)[(-16 * count):]) # 16 bits per char as in C# a string uses 2 byes per char

    def getInt32(self, data):
        ''' 4 bytes, return as int (unsigned if needed) '''

        return int(bin(data)[-32:], 2)

    def getByteAsInt(self, data):
        ''' pull first byte from value return as an int '''

        return int(bin(data)[-8:], 2)

    def getShortAsInt(self, data):
        ''' pull first two bytes from value return as an int (short) '''

        return int(bin(data)[-16:], 2)

    def checkPacket_test(self, data, seed=None, rots=0):
        ''' For Testing purposes '''

       #for _ in range(rots):
       #     self.
        if seed is not None:
            self.XOR32_seed = seed

        self.checkPacket(data)

if __name__ == "__main__":
    pass
    #test_decrypt_packet_header(b'5787d026b6e0ef136312')

    class dummy(object):
        def __init__(self):
            self.outbound = False

    adummy = dummy()

    aTCP = TCP(adummy)
    #aTCP.checkPacket(b'270339c654ea8a718af8637d0264359e52a015496ad379df76b7edb7f3ef')
    #aTCP.checkPacket(b'4c4b624790f9c0371b87')
    aTCP.checkPacket_test(b'5af8d004c077cd3a26a45dece23873a8b0f43ac9cc07fc67cbe980437ad26442164cddefc80ca979ef29ddf2e2efeef69896ba91e09995e1e04fae067a249c27ee113e58f23959904f6be7690665bcc354b8354069efaf4310ce925b8c20800b2f79516abad40eeca93fe5409cda08c1d8d17e209cd6ce68731cb22c027e184a62bdea4baf9282bb9766d53e4d8eb98e0884348706754c363ef78751f5be324e571ac9fc00d4a63d0356f78cfaec65fab1e3c4ba528421f994fd7b31f429318c78c8aa904ee93fb561f2793ec203efccc924e738036c4b1aef7710ce563b58f6c51dd818c0a9bbaf8cd9e46c2bcd5e743ef9e777e932357b2a7e63dadb0bf2b29235e43503796dade77c8206ceb0af89f7bf407667dfef4f76d3be30b92420b2373e765ad38b36a6d50b4122c228b9c473893852e461843ffb670581c5c01a6dd5022c24972ebf7409d5fde3156e6af580a38ef8ae17766621b158e1accd1907cb1fb6eac3fa991a58b5235e1e3517b05a4d952474dbe3b9aea503dc4f8495d9db7bf5d25f4c4e8bd262747927aec11b6b9ad6588ab31d8877f742ec84521dce76fb4a4602bdd09a86098b187546196925c87bc238598b3c43a988edbc9a7285fdfeeac973472855011f7250827e16a03e01d8e48f71b10d2eb506657f6be52719789afa8abccc5d3aea2bf05c0d48e95299e9b0c277170223b951d20c65f25902c0a4173f0cd9b62feb49da1a25780ae3fda84296569c40e57bbc341fdca299138b9dc24c70182b15da01a2682f56855512b6879dc4b63867a8b0de41498c3ece13fe29abe2bd95df4d75985b71ee3725aefd7b5b484e0cb97e39a7684438244513afd7a6c346618a6576118e7f31aca9e2daa62ab19b47f0cf9ce94251a17ba69d6be397ec68942688b7c360044f24f495548017ab1e7175d4a3b750e4245cd838bb0a21bce3011214e7b7c97b038b445d154947bb8eb52b7a16ca06f9f4004cb3e70dd5de14d17db1c5c7fbfad16f66f3fa5f28405f0ca30b1a07ded4e067e341e9421d51250982ff3c34f751b4902880092b19a048ea1b3cc248a231061b78caca82e8e183af0a05729e0878fb6f956e2710b59ebedb7f3be0d24d11b6cff2f7d2f2e4a86f8154cf98e4c447fcb27608a8055c3876b42ff2e5644114210ece02e5ff1fcf61fcb107f46055d4cdacd4b013da5d6c9766857123624245c8f3f340b25f16af0fd585ce3918d2fdb407798249bf838ad7862041dec46ae98b0b3f863170dd62d35dd9bbb61626e0fe8c1c559cf9fe129096f2985d03b28679217cac17d93e361bbff138fbd8983152114fb1169f0fed38e9f189c0afb6982b05d79a2d5b25a310381961ba3335c7f0c78caf21b3b9a5a2464a047bb1861553f604762a09cb7b381ebfbbc59c2fad655f26a69d4a801873133898469025176e213f4010cc5b2eb5e5eb7d9c5fb36af262beb7f4055c92c5d3bcd5f1ac89206c9978663d9cd1b082ced17dc0cea91fbade6489163e219db111aabfa1b801b4c75859db46b94fc59ce56038cb4207049de7dd6204037ae532565bf93c13c156b415a1749a428ebcf7cf9240fab51f6073e6b5b5b95cb60bdd4e5bdeccc419831bb9b578cfe1b00c74ad08e71c2d0b88ba637c740a60ecdd29ff3d35a1daac73bd61376019ae508bfa9e8b10104a34435a1baeefdcb1a6f029e03f69fa5c7fd93733e0dc724f50f00591c815621bf6a5939539a55b8dbe9c099ab20eb5e3db4d7ed83e21f828948c9e47b974d0c015a77690831d9228e5bb73fae3adc90ab6d7527d0ce96b61e8a9419befb97bc42c36854455657cdbfedfd05af512e988c7781a42c87fe203f1f168e78805e7e15e7326f0821192778425daa97253ac10975eab0dcf7a7bf445e483fdb870abdac9d52dc0de4e9729478f0bb83c46d708fe2707b4291c2cbd2bb0abf6e3010aa2229653e9e12cf1b8014ee441ac5f188c301d898d9a19628f61b5', seed=23896252)
