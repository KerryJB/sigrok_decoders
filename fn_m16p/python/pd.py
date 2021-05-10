''' FN_M16P serial protocol decoder'''
##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2021 Kerry Burton <KerryKJB1@gmail.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd

    # Import sets of strings for labeling I/O packets and their fields
from .fn_m16p_messages import field_label, packet_msg,                    \
                              list_A,  list_B,  list_C, list_D,   list_E, \
                              list_LS, list_MS, list_O, list_40RX

#                             ==========================
#                             FN_M16P DATA PACKET FORMAT
#                             ==========================
#                                                  Parameter        Checksum
#       START    VER     LEN     CMD    FEED     MSB     LSB    CHK1    CHK2     END
#     +-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
#     | 0x7E  | 0xFF  | 0x06  |[DATA] | 0 or 1|[DATA] |[DATA] |[CALC] |[CALC] | 0xEF  |
#     +-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+

    # Byte offsets within each packet
# START = 0, VER = 1, LEN = 2, FEED = 4, CHK1 = 7, CHK2 = 8, END = 9
CMD = 3
MSB = 5
LSB = 6

START_BYTE = 0x7E
END_BYTE   = 0xEF

def expand_str( org_str, my_msb, my_lsb ):
    ''' "Expand" data packet labels by replacing placeholders with actual values'''

    my_12bit = ((my_msb & 0x0F) << 8) + my_lsb   # Lower 12 bits of 2-byte parameter
    my_word  = (my_msb << 8) + my_lsb            # Full 16-bit value of parameter
    my_str   = org_str[:]                        # Start with copy of original string

        # Perform marker/placeholder substitutions that rely on indexed strings
    if my_str.find('^LA') >= 0:
        my_str = my_str.replace('^LA',  list_A[my_lsb])
    if my_str.find('^LB') >= 0:
        my_str = my_str.replace('^LB',  list_B[my_lsb])
    if my_str.find('^LC') >= 0:
        my_str = my_str.replace('^LC',  list_C[my_lsb])
    if my_str.find('^LD') >= 0:
        my_str = my_str.replace('^LD',  list_D[my_lsb])
    if my_str.find('^LE') >= 0:
        my_str = my_str.replace('^LE',  list_E[my_lsb])
    if my_str.find('^LS') >= 0:
        my_str = my_str.replace('^LS',  list_LS[my_lsb])
    if my_str.find('^MA') >= 0:
        my_str = my_str.replace('^MA',  list_A[my_msb])
    if my_str.find('^MS') >= 0:
        my_str = my_str.replace('^MS',  list_MS[my_msb%16])

        # Perform marker/placeholder substitutions that don't use indexed strings
    my_str = my_str.replace('^MH',  str(my_msb >> 4))
    my_str = my_str.replace('^MLL', str(my_12bit))
    my_str = my_str.replace('^L',   str(my_lsb)) # Process single-character placeholders LAST
    my_str = my_str.replace('^M',   str(my_msb))
    my_str = my_str.replace('^W',   str(my_word))

    return my_str                                # After making all applicable substitutions,
                                                 # return expanded string


class Decoder(srd.Decoder):
    ''' Main class of FN_M16P serial protocol decoder'''
    api_version = 3
    id          = 'fn_m16p'
    name        = 'FN-M16P'
    longname    = 'FN-M16P module (MP3/WAV player)'
    desc        = 'FN-M16P module (MP3/WAV player) serial protocol.'
    license     = 'gplv2+'
    inputs      = ['uart']
    outputs     = []         # ['fn_m16p'] -- For future use???
#    channels          = ** No extra channels needed beyond those defined for the UART decoder **
#    optional_channels = ** NONE **
#    options           = ** No extra options needed beyond those defined for the UART decoder **

    annotations = (
# ------  Identifier --- Description -------- Meaning --------------------------------------------
# FIELDS
        ('rx-unknown',  'RX Unknown'   ),   #  0 - Unexpected data byte
        ('tx-unknown',  'TX Unknown'   ),   #  1
        ('rx-start',    'RX Start Byte'),   #  2 - Start Byte: Always 0x7E
        ('tx-start',    'TX Start Byte'),   #  3
        ('rx-ver',      'RX Version'   ),   #  4 - Version: 0xFF by default
        ('tx-ver',      'TX Version'   ),   #  5
        ('rx-len',      'RX Length'    ),   #  6 - Length: 6 bytes [ver+len+cmdcode+feed+parm(2)]
        ('tx-len',      'TX Length'    ),   #  7
        ('rx-cmdcode',  'RX Cmd Byte'  ),   #  8 - Command code: Can range from 0x01 to 0x4F
        ('tx-cmdcode',  'TX Cmd Byte'  ),   #  9
        ('rx-feed',     'RX Feedback'  ),   # 10 - Feedback flag: 0x00 = Don't send, 0x01 = Send
        ('tx-feed',     'TX Feedback'  ),   # 11
        ('rx-parm',     'RX Param'     ),   # 12 - Two Parameter bytes: MSB then LSB
        ('tx-parm',     'TX Param'     ),   # 13
        ('rx-chk',      'RX Checksum'  ),   # 14 - (Optional) Two Checksum bytes: MSB then LSB
        ('tx-chk',      'TX Checksum'  ),   # 15
        ('rx-end',      'RX End Byte'  ),   # 16 - End Byte: Always 0xEF
        ('tx-end',      'TX End Byte'  ),   # 17
# PACKETS
        ('rx-packet',   'RX Packet'    ),   # 18 - Overall packet (command/query/report/feedback)
        ('tx-packet',   'TX Packet'    ),   # 19
    )
    annotation_rows = (
# ------  Identifier --- Description --- Annotation class index/ices -----------
        ('rx-fields',   'RX Fields',    ( 0,  2,  4,  6,  8, 10, 12, 14, 16,)),
        ('rx-feedback', 'RX Feedback',  (18,                                )),

        ('tx-fields',   'TX Fields',    ( 1,  3,  5,  7,  9, 11, 13, 15, 17,)),
        ('tx-commands', 'TX Commands',  (19,                                )),
    )
#   binary = ** N/A **
    tags = ['Audio']

###############################
####### Decoder methods #######
###############################
    def __init__(self):
        self.out_ann = None                      # To avoid pylint message W0201
        self.reset()


    def reset(self):
        '''Initialize RX/TX channel-specific values'''
                          # RX      TX
        self.packet_ss   = [-1,     -1    ]      # Set Start Sample numbers out of range
        self.packet_es   = [-1,     -1    ]      # Set End Sample numbers out of range
        self.packet_data = [[],     []    ]      # Clear out data bytes for packets
        self.state       = ['IDLE', 'IDLE']      # Set states to "Not currently in a packet"


    def reset_channel(self, rxtx):
        '''Initialize channel-specific values for a single channel (RX or TX)'''
        self.packet_ss[rxtx]   = -1              # Set Start Sample number out of range
        self.packet_es[rxtx]   = -1              # Set End Sample number out of range
        self.packet_data[rxtx] = []              # Clear out data bytes for packet
        self.state[rxtx]       = 'IDLE'          # Set state to "Not currently in a packet"


    def start(self):
        '''Not sure exactly when this is called...'''
        self.out_ann = self.register(srd.OUTPUT_ANN)


    def process_idle_byte(self, start_smpl, end_smpl, rxtx, pdata):
        '''Handle a byte received while specified channel is in the IDLE state'''
        if pdata == START_BYTE:                  # Received a Start Byte?
            self.put( start_smpl, end_smpl, self.out_ann, [2+rxtx, field_label[1]] )
                                                 #  Yes, label the Start byte
            self.packet_ss[rxtx] = start_smpl    #   Remember packet's starting sample number
            self.packet_data[rxtx].append(pdata) #   Add start byte to packet data
            self.state[rxtx] = 'PACKET'          #   Change to "inside a packet" state
        else:                                    #  No (not a Start Byte)...
            self.put( start_smpl, end_smpl, self.out_ann, [0+rxtx, field_label[0]] )
                                                 #   Label the unexpected byte


    def gen_packet_label(self, rxtx):
        '''Controller method for generating a single label for a given data packet'''
                                                 # Copy useful numbers
        cmd = self.packet_data[rxtx][CMD]        #  Command Code
        msb = self.packet_data[rxtx][MSB]        #  MSB of parameter
        lsb = self.packet_data[rxtx][LSB]        #  LSB of parameter

        if (cmd, rxtx) in packet_msg:            # Does message collection contain an
                                                 # entry that matches packet's Command
                                                 # Code and RX/TX direction?
            msg = packet_msg[cmd, rxtx]          #  Yes, init local reference variable
            if msg[0].find("^") < 0:             #   Does the entry contain any "markers"
                                                 #   to be replaced?
                output = msg                     #    No, use entry as-is
            elif msg[0] == '^LO':                #    Yes, is the entry for reporting
                                                 #    Online devices?
                output = list_O[lsb]             #     Yes, use separate list of device
                                                 #     combinations
            elif msg[0] == '^LX':                #     No, is the entry for reporting
                                                 #     eXceptions/errors?
                output = list_40RX[lsb]          #      Yes, use separate list of errors
            else:                                #      No, replace "standard" markers...
                output = []                      #       Start with empty string list
                for msg_str in msg:              #       For each str in matching entry...
                    output.append( expand_str(msg_str, msb, lsb) )
                                                 #        Add "expanded" version to output str list

        else:                                    #  No (no matching message entry)
            output = packet_msg[0xFF, rxtx]      #   Use the generic "Unknown Feedback
                                                 #   / Command" message, based on RX/TX
            # The one-and-only (packet level) output statement
        self.put(self.packet_ss[rxtx],self.packet_es[rxtx],self.out_ann,[18+rxtx,output])


    def process_packet_byte(self, start_smpl, end_smpl, rxtx, pdata):
        '''Handle a byte received while specified channel is in the PACKET state'''
        end_of_packet = False                    #   Yes, assume we're NOT at end of packet
        self.packet_data[rxtx].append(pdata)     #    Add new byte to packet data
        pkt_len = len(self.packet_data[rxtx])    #    Get # of bytes in packet so far
        if pkt_len in (2, 3, 4, 5, 6, 7):        #    Received intermediate data byte?
            ann_row = (pkt_len * 2) + rxtx       #     Yes, calculate appropriate annotation index
            self.put( start_smpl, end_smpl, self.out_ann, [ann_row, field_label[pkt_len]] )
                                                 #      Label the Ver/Len/Cmd/Feed/MSB/LSB byte
        elif pkt_len == 8:                       #    8 bytes of packet data so far?
            if pdata == END_BYTE:                #     Yes, is 8th byte an End Byte?
                                                 #      (Checksum bytes are optional)
                end_of_packet = True             #      Yes, remember to close the packet
            else:                                #      No...
                self.put( start_smpl, end_smpl, self.out_ann, [14+rxtx, field_label[8]] )
                                                 #       Label the Checksum MSB byte
        elif pkt_len == 9:                       #    9 bytes of packet data so far?
            self.put( start_smpl, end_smpl, self.out_ann, [14+rxtx, field_label[9]] )
                                                 #     Yes, label the Checksum LSB byte
        elif pkt_len == 10:                      #    10 bytes of packet data so far?
            if pdata == END_BYTE:                #     Yes, is byte #10 an End Byte?
                end_of_packet = True             #      Yes, remember to close the packet
            else:                                #      No...
                self.put( start_smpl, end_smpl, self.out_ann, [ 0+rxtx, field_label[15]] )
                                                 #       Label the out-of-place data byte

        if end_of_packet:                        #    8th (or 10th) byte was an End Byte?
            self.put( start_smpl, end_smpl, self.out_ann, [16+rxtx, field_label[10]] )
                                                 #     Yes, label the End Byte
            self.packet_es[rxtx] = end_smpl      #      Remember packet's ending sample number
            self.gen_packet_label(rxtx)          #      Generate label for the overall packet

        if end_of_packet or pkt_len >= 10:       #    Packet ended cleanly (or was corrupted)?
            self.reset_channel(rxtx)             #     Yes, reset values for RX/TX "channel"


    def decode(self, start_smpl, end_smpl, data):
        '''Main FN_M16P protocol decoder method, called by sigrokdecoder core when the UART
           decoder has assembled a packet'''
        ptype, rxtx, pdata = data

            # Ignore all UART packets except actual data packets
        if ptype != 'DATA':
            return
            # We're only interested in byte values (not individual bits)
        pdata = pdata[0]

        if self.state[rxtx] == 'IDLE':           # Waiting for an FN_M16P packet to start?
            self.process_idle_byte(start_smpl, end_smpl, rxtx, pdata)
                                                 #  Yes, handle byte received while "IDLE"

        elif self.state[rxtx] == 'PACKET':       #  No, currently inside an FN_M16P packet?
            self.process_packet_byte(start_smpl, end_smpl, rxtx, pdata)
                                                 #  Yes, handle byte received within the packet
