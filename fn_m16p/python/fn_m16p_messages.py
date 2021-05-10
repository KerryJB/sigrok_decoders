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

RX = 0
TX = 1

field_label = {
    0:  ['Unexpected',     '???',     '??',  '?' ],

    1:  ['Start Byte',     'Start',   'St',  'S' ],
    2:  ['Version',        'Ver',            'V' ],
    3:  ['Length',         'Len',            'L' ],
    4:  ['Command Code',   'CmdCd',   'CC',  'C' ],
    5:  ['Feedback',       'Fdbk',    'Fb',  'F' ],
    6:  ['Param MSB',      'P MSB',   'PM',  'P' ],
    7:  ['Param LSB',      'P LSB',   'PL',  'P' ],
    8:  ['Chksum MSB',     'C MSB',   'CM',  'C' ],
    9:  ['Chksum LSB',     'C LSB',   'CL',  'C' ],
    10: ['End Byte',       'End',            'E' ],

    15: ['Frame Error',    'Frm Err', 'FE'       ]
}


# ====== Legend for placeholder markers ======
#   ^L   = Value of LSB
#   ^M   = Value of MSB
#   ^W   = (MSB << 8) + LSB                           # W stands for "Word"
#   ^LA  = Use value of LSB as index to list_A[]
#   ^LB  = Use value of LSB as index to list_B[]
#   ^LC  = Use value of LSB as index to list_C[]
#   ^LD  = Use value of LSB as index to list_D[]
#   ^LE  = Use value of LSB as index to list_E[]
#   ^LO  = Use value of LSB as index to list_O[]
#   ^LS  = Use value of LSB as index to list_LS[]
#   ^LX  = Use value of LSB as index to list_40RX[]
#   ^MA  = Use value of MSB as index to list_A[]
#   ^MH  = Value of 4 High bits of MSB
#   ^MLL = ((4 low bits of MSB) << 8) + LSB
#   ^MS  = Use value of MSB as index to list_MS[]

packet_msg = {
    (0x00, RX): ['Feedback Message',         'Fdbk Msg',          'Fdbk'        ],
    (0x00, TX): ['Command Message',          'Cmd Msg',           'Cmd'         ],

    (0x01, TX): ['Play Next Track',          'Next Track',        'Next'        ],
    (0x02, TX): ['Play Previous Track',      'Prev Track',        'Prev'        ],
    (0x03, TX): ['Play Track /^W',           'Track /^W',         '/^W'         ],
    (0x04, TX): ['Increase Volume',          'Volume Up',         'Vol +'       ],
    (0x05, TX): ['Decrease Volume',          'Volume Down',       'Vol -'       ],
    (0x06, TX): ['Set Volume to ^W',         'Volume = ^W',       'Vol ^W'      ],
    (0x07, TX): ['Set Equalization to ^LE',  'Set EQ to ^LE',     'EQ=^LE'      ],
    (0x08, TX): ['Loop Device Track ^W',     'Loop Dev Trk ^W',   'Lp DT ^W'    ],
    (0x09, TX): ['Play from ^LD',            'Use ^LD',           '^LD'         ],
    (0x0A, TX): ['Go to Sleep',              'Sleep!'                           ],
    (0x0B, TX): ['[Reserved]',               '[Rsvd]'                           ],
    (0x0C, TX): ['Reset Module',             'Reset',             'Rst'         ],
    (0x0D, TX): ['Play'                                                         ],
    (0x0E, TX): ['Pause'                                                        ],
    (0x0F, TX): ['Play Track /^M/^L',        'Play /^M/^L',       '/^M/^L'      ],
    (0x10, TX): ['Amplify ^MA, Gain ^L',     'Amp ^MA, Gn ^L'                   ],
    (0x11, TX): ['Set Rpt All Tracks ^LA',   'Repeat All ^LA',    'Rpt All ^LA' ],
    (0x12, TX): ['Play Track /MP3/^W',       'Track /MP3/^W',     '/MP3/^W'     ],
    (0x13, TX): ['Play Track /ADVERT/^W',    'Trk /ADVERT/^W',    'Ad ^W'       ],
    (0x14, TX): ['Play Track /^MH/^MLL',     'Trk /^MH/^MLL',     '/^MH/^MLL'   ],
    (0x15, TX): ['Return from Ad Track',     'Return from Ad',    'End Ad'      ],
    (0x16, TX): ['Stop All Playback',        'Stop Playback',     'Stop'        ],
    (0x17, TX): ['Repeat Folder /^L',        'Repeat /^L',        'Rpt /^L'     ],
    (0x18, TX): ['Random Play All Tracks',   'Random Play All',   'Rndm All'    ],
    (0x19, TX): ['Set Repeat Track ^LB',     'Repeat Track ^LB',  'Rpt Trk ^LB' ],
    (0x1A, TX): ['Turn DAC (Line Out) ^LB',  'Turn DAC ^LB',      'DAC ^LB'     ],

    (0x3A, RX): ['^LC was Plugged In',       '^LC Plugged',       '^LC In'      ],
    (0x3B, RX): ['^LC was Unplugged',        '^LC Unplugged',     '^LC Out'     ],
    (0x3C, RX): ['USB Track ^W Finished',    'USB Trk ^W Fin',    'U Trk ^W F'  ],
    (0x3D, RX): ['SD Track ^W Finished',     'SD Trk ^W Fin',     'S Trk ^W F'  ],
    (0x3E, RX): ['Flash Track ^W Finished',  'Flsh Trk ^W Fin',   'F Trk ^W F'  ],

    (0x3F, TX): ['Query Online Devices',     'Qry Devices',       'Qry Devs'    ],
    (0x3F, RX): ['^LO',                                                         ],

    (0x40, RX): ['^LX',                                                         ],
    (0x41, RX): ['Command Acknowledged',     'Acknowledged',      'ACK'         ],

    (0x42, TX): ['Get Current Status',       'Cur Status = ?',    'Stat=?'      ],
    (0x42, RX): ['Status:^MS / ^LS',         '^MS / ^LS'                        ],

    (0x43, TX): ['Get Current Volume',       'Cur Volume = ?',    'Vol=?'       ],
    (0x43, RX): ['Current Volume = ^W',      'Volume = ^W',       'Vol=^W'      ],

    (0x44, TX): ['Get Equalization',         'Current EQ=?',      'EQ=?'        ],
    (0x44, RX): ['Equalization = ^LE',       'Current EQ = ^LE',  'EQ=^LE'      ],

# 0x45 not mentioned in datasheet
# 0x46 not mentioned in datasheet

    (0x47, TX): ['USB:/ Track Count?',       'USB:/ Trk Cnt?',    'USB:/ Trks?' ],
    (0x47, RX): ['USB:/ Track Count=^W',     'USB:/ Trk Cnt=^W',  'U:/ Trks=^W' ],

    (0x48, TX): ['SD:/ Track Count?',        'SD:/ Trk Cnt?',     'SD:/ Trks?'  ],
    (0x48, RX): ['SD:/ Track Count=^W',      'SD:/ Trk Cnt=^W',   'SD:/ Trks=^W'],

# 0x49 not mentioned in datasheet
# 0x4A not mentioned in datasheet

    (0x4B, TX): ['Get USB Current Track',    'USB Cur Trk?',      'USB Trk?'    ],
    (0x4B, RX): ['USB Current Track=^W',     'USB Cur Trk=^W',    'USB Trk=^W'  ],

    (0x4C, TX): ['Get SD Current Track',     'SD Cur Trk?',       'SD Trk?'     ],
    (0x4C, RX): ['SD Current Track=^W',      'SD Cur Trk=^W',     'SD Trk=^W'   ],

# 0x4D not mentioned in datasheet

    (0x4E, TX): ['Track Cnt in Folder /^W?', 'Trks in /^W?',      '/^W Trks?'   ],
    (0x4E, RX): ['Tracks in Folder=^W',      'Fldr Trks=^W',      'F Trks=^W'   ],

    (0x4F, TX): ['Query Folder Count',       'Folder Count?',     'Fldr Cnt?'   ],
    (0x4F, RX): ['Folder Count = ^W',        'Folders = ^W',      'Fldrs=^W'    ],


    (0xFF, TX): ['Unknown Command',          'Unknown Cmd',       'Unk Cmd'     ],
    (0xFF, RX): ['Unknown Feedback',         'Unknown Fdbk',      'Unk Fdbk'    ]
}


list_A  = ['OFF',      'ON'                                              ]  # Normal order for 0,1
list_B  = ['ON',       'OFF'                                             ]  # Reverse order for 0,1
list_C  = ['',         'USB Flash', 'SD Card', '',     'USB Cable'       ]  # Connections
list_D  = ['',         'USB Flash', 'SD Card'                            ]  # Devices
list_E  = ['Normal',   'Pop',       'Rock',    'Jazz', 'Classic',  'Bass']  # Equalization modes
list_LS = ['Stopped',  'Playing',   'Paused'                             ]  # Status mode
list_MS = ['Sleeping', 'USB Drive', 'SD Card'                            ]  # Status device

# ============================

list_O  =   [       # Online devices
              ['Online: [None]',                        ],
              ['Online: USB Drive',       'On: USB'     ],
              ['Online: SD Card',         'On: SD'      ],
              ['Online: USB+SD',          'On: U+S'     ],
              ['Online: PC',                            ],
              ['Online: PC+USB',          'On: P+U'     ],
              ['Online: PC+SD',           'On: P+S'     ],
              ['Online: PC+USB+SD',       'On: P+U+S'   ],
              ['Online: Flash',                         ],
              ['Online: Flash+USB',       'On: F+U'     ],
              ['Online: Flash+SD',        'On: F+S'     ],
              ['Online: Flash+USB+SD',    'On: F+U+S'   ],
              ['Online: Flash+PC',        'On: F+P'     ],
              ['Online: Flash+PC+USB',    'On: F+P+U'   ],
              ['Online: Flash+PC+SD',     'On: F+P+S'   ],
              ['Online: Flash+PC+USB+SD', 'On: F+P+U+S' ]
            ]

list_40RX = [       # eXceptions / errors
              ['[Reserved]',              '[Rsvd]'                      ],
              ['Not Initialized',         'Not Ready',      'Not Rdy'   ],
              ['Module is Sleeping',      'Module Asleep',  'Asleep'    ],
              ['Frame Error',             'Frame Err',      'Frm Err'   ],
              ['Checksum Mismatch',       'Bad CheckSum',   'ChkSm Err' ],
              ['Track # Out of Bounds',   'Bad Track #',    'Bad Trk#'  ],
              ['Track Not Found',         'No Such Track',  'Not Fnd'   ],
              ['Must Play to Insert Ad',  'Can\'t Play Ad', 'Ad Err'    ],  # (My interpretation)
              ['Error Reading SD Card',   'SD Card Error',  'SD Err'    ],
              ['[Reserved]',              '[Rsvd]'                      ],
              ['Entered Sleep Mode',      'Entered Sleep',  'Enter Slp' ]   # Different than
                                                                            # 'Module is Sleeping'?
            ]
